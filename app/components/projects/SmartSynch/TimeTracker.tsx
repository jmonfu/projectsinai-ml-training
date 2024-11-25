'use client';

import { useState, useEffect, useCallback } from 'react';
import { Button } from '../../../components/common/Button';

interface TimeTrackerProps {
  taskId: string;
  initialTime?: number;
  onTimeUpdate?: (seconds: number) => void;
}

export function TimeTracker({ taskId, initialTime = 0, onTimeUpdate }: TimeTrackerProps) {
  const [isRunning, setIsRunning] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(initialTime);

  const updateTime = useCallback((newTime: number) => {
    setElapsedTime(newTime);
    // Use requestAnimationFrame to defer the update
    if (onTimeUpdate) {
      requestAnimationFrame(() => onTimeUpdate(newTime));
    }
  }, [onTimeUpdate]);

  useEffect(() => {
    let intervalId: NodeJS.Timeout | undefined;

    if (isRunning) {
      intervalId = setInterval(() => {
        updateTime(elapsedTime + 1);
      }, 1000);
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [isRunning, elapsedTime, updateTime]);

  const formatTime = (seconds: number): string => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins
      .toString()
      .padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleToggle = () => {
    if (isRunning) {
      // When stopping, ensure we save the final time
      onTimeUpdate?.(elapsedTime);
    }
    setIsRunning(!isRunning);
  };

  return (
    <div className="flex items-center gap-3">
      <div className="font-mono text-lg bg-gray-100 px-3 py-1 rounded text-gray-900 font-medium">
        {formatTime(elapsedTime)}
      </div>
      <Button
        onClick={handleToggle}
        className={`text-white px-4 py-2 ${
          isRunning 
            ? 'bg-red-500 hover:bg-red-600' 
            : 'bg-blue-500 hover:bg-blue-600'
        }`}
      >
        {isRunning ? 'Stop' : 'Start'}
      </Button>
    </div>
  );
}