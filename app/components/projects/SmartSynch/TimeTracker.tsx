'use client';

import { useState, useEffect, useCallback } from 'react';
import { Button } from '../../../components/common/Button';

interface TimeTrackerProps {
  taskId: string;
  timeSpent: number;
  onTimeUpdate: (seconds: number) => void;
  onStart: () => void;
  isActive?: boolean;
}

export function TimeTracker({ taskId, timeSpent, onTimeUpdate, onStart, isActive = false }: TimeTrackerProps) {
  const [seconds, setSeconds] = useState(timeSpent);
  const [isRunning, setIsRunning] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isRunning) {
      interval = setInterval(() => {
        setSeconds(s => {
          const newSeconds = s + 1;
          requestAnimationFrame(() => onTimeUpdate?.(newSeconds));
          return newSeconds;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isRunning, onTimeUpdate]);

  useEffect(() => {
    if (!isActive && isRunning) {
      setIsRunning(false);
    }
  }, [isActive]);

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
    if (!isRunning) {
      setIsRunning(true);
      onStart();
    } else {
      handleStop();
    }
  };

  const handleStop = () => {
    setIsRunning(false);
    onTimeUpdate(seconds);
  };

  return (
    <div className="space-y-2">
      <div className="flex items-center gap-3">
        <div className="font-mono text-lg bg-gray-100 px-3 py-1 rounded text-gray-900 font-medium">
          {formatTime(seconds)}
        </div>
        <Button
          onClick={handleToggle}
          className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2"
        >
          {isRunning ? 'Stop' : 'Start'}
        </Button>
      </div>
    </div>
  );
}