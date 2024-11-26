"use client";

import { useEffect, useState } from 'react';
import { useSearchParams } from 'next/navigation';

export default function TimerPage() {
  const [seconds, setSeconds] = useState(0);
  const [taskName, setTaskName] = useState('');
  const searchParams = useSearchParams();

  useEffect(() => {
    setTaskName(searchParams.get('name') || '');

    const handleMessage = (event: MessageEvent) => {
      if (event.data.type === 'UPDATE_TIME') {
        setSeconds(event.data.seconds);
        setTaskName(event.data.taskName);
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  const handleStop = () => {
    window.opener?.postMessage('stop', '*');
    window.close();
  };

  const formatTime = (secs: number) => {
    const hours = Math.floor(secs / 3600);
    const minutes = Math.floor((secs % 3600) / 60);
    const remainingSeconds = secs % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  return (
    <div className="p-2 h-screen bg-white overflow-hidden select-none">
      <div className="text-xs font-medium text-gray-500 truncate mb-1">
        {taskName}
      </div>
      <div className="text-lg font-bold text-gray-900">
        {formatTime(seconds)}
      </div>
      <button
        onClick={handleStop}
        className="w-full bg-red-500 hover:bg-red-600 text-white text-sm font-medium py-1.5 px-2 rounded mt-1"
      >
        STOP
      </button>
    </div>
  );
} 