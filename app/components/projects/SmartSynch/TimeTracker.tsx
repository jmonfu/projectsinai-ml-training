'use client';

import { useState, useEffect, useCallback } from 'react';
import { Button } from '../../../components/common/Button';

interface TimeTrackerProps {
  taskId: string;
  initialTime: number;
  onTimeUpdate: (seconds: number) => void;
  onStart: () => void;
  task?: {
    timeRecords?: Array<{
      timestamp: string;
      seconds: number;
    }>;
  };
}

export function TimeTracker({ taskId, initialTime = 0, onTimeUpdate, onStart, task }: TimeTrackerProps) {
  const [mounted, setMounted] = useState(false);
  const [isRunning, setIsRunning] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(initialTime);

  const updateTime = useCallback((newTime: number) => {
    setElapsedTime(newTime);
    if (onTimeUpdate) {
      requestAnimationFrame(() => onTimeUpdate(newTime));
    }
  }, [onTimeUpdate]);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    let intervalId: NodeJS.Timeout | undefined;

    if (isRunning) {
      intervalId = setInterval(() => {
        setElapsedTime(prev => prev + 1);
      }, 1000);
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId);
      }
    };
  }, [isRunning]);

  if (!mounted) {
    return null;
  }

  const formatTime = (seconds: number): string => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins
      .toString()
      .padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const formatDate = (timestamp: string): string => {
    const date = new Date(timestamp);
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
  };

  const handleToggle = () => {
    if (isRunning) {
      const stopTimestamp = new Date().toISOString();
      console.log('Stopping timer:', { elapsedTime, stopTimestamp });
      onTimeUpdate?.(elapsedTime);
    } else {
      console.log('Starting timer');
    }
    setIsRunning(!isRunning);
  };

  return (
    <div className="space-y-2">
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
      {/* Add this to show time records */}
      {task?.timeRecords && task.timeRecords.length > 0 && (
        <div className="mt-2 text-xs text-gray-500">
          <div>
            Last stopped at: {formatDate(task.timeRecords[task.timeRecords.length - 1].timestamp)} (
            {Math.floor(task.timeRecords[task.timeRecords.length - 1].seconds / 60)}m{' '}
            {task.timeRecords[task.timeRecords.length - 1].seconds % 60}s)
          </div>
        </div>
      )}
    </div>
  );
}