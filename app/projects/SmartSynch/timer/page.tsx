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
    <div className="p-3 h-screen bg-white">
      <div className="text-sm font-medium text-gray-500 truncate">
        {taskName}
      </div>
      <div className="text-xl font-bold text-gray-900 my-1">
        {formatTime(seconds)}
      </div>
      <button
        onClick={handleStop}
        className="w-full bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-3 rounded"
      >
        STOP
      </button>
    </div>
  );
} 