import React, { useState, useEffect } from 'react';

interface FloatingTimerProps {
  seconds: number;
  taskName: string;
  onStop: () => void;
  isRunning: boolean;
}

export function FloatingTimer({ seconds, taskName, onStop, isRunning }: FloatingTimerProps) {
  const [timerWindow, setTimerWindow] = useState<Window | null>(null);

  useEffect(() => {
    if (isRunning && !timerWindow) {
      const width = 50;
      const height = 50;
      const left = window.screenX + window.outerWidth - width;
      const top = window.screenY + window.outerHeight - height;
      
      const newWindow = window.open(
        `${window.location.origin}/projects/SmartSynch/timer?name=${encodeURIComponent(taskName)}`,
        'timer',
        `width=${width},height=${height},left=${left},top=${top},` +
        'chrome=no,centerscreen=yes,resizable=no,scrollbars=no,' +
        'status=no,toolbar=no,menubar=no,location=no'
      );
      
      if (newWindow) {
        setTimerWindow(newWindow);
        // Immediately send initial time
        setTimeout(() => {
          newWindow.postMessage({ type: 'UPDATE_TIME', seconds, taskName }, '*');
        }, 0);
      }
    }

    return () => {
      timerWindow?.close();
    };
  }, [isRunning]);

  useEffect(() => {
    if (!timerWindow) return;
    timerWindow.postMessage({ type: 'UPDATE_TIME', seconds, taskName }, '*');
  }, [timerWindow, seconds, taskName]);

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data === 'stop') {
        onStop();
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, [onStop]);

  return null;
}

const formatTime = (secs: number) => {
  const hours = Math.floor(secs / 3600);
  const minutes = Math.floor((secs % 3600) / 60);
  const remainingSeconds = secs % 60;
  return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`;
}; 