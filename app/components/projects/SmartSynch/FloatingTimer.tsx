import React from 'react';
import { createPortal } from 'react-dom';

interface FloatingTimerProps {
  seconds: number;
  taskName: string;
  onStop: () => void;
}

export function FloatingTimer({ seconds, taskName, onStop }: FloatingTimerProps) {
  const formatTime = (secs: number) => {
    const hours = Math.floor(secs / 3600);
    const minutes = Math.floor((secs % 3600) / 60);
    const remainingSeconds = secs % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  return createPortal(
    <div className="fixed bottom-4 right-4 bg-white rounded-lg shadow-lg p-4 border border-gray-200 w-64 animate-in slide-in-from-right">
      <div className="text-sm font-medium text-gray-500 truncate">{taskName}</div>
      <div className="text-2xl font-bold text-gray-900 my-2">{formatTime(seconds)}</div>
      <button
        onClick={onStop}
        className="w-full bg-red-500 hover:bg-red-600 text-white font-medium py-2 px-4 rounded"
      >
        STOP
      </button>
    </div>,
    document.body
  );
} 