'use client';

import { TASK_CATEGORIES, TaskCategory } from '../../../lib/categories';
import { Button } from '../../../components/common/Button';
import { Pencil, Trash2, Flag } from 'lucide-react';
import { TimeTracker } from './TimeTracker';
import { useEffect, useState } from 'react';
import { FloatingTimer } from './FloatingTimer';

interface Task {
  id: string;
  title: string;
  description: string;
  category: TaskCategory;
  priority: 'high' | 'medium' | 'low';
  createdAt: string;
  timeSpent?: number;
  timeRecords?: Array<{timestamp: string, seconds: number}>;
}

interface TaskListProps {
  tasks: Task[];
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onTimeUpdate?: (taskId: string, seconds: number, timeRecords: Array<{timestamp: string, seconds: number}>) => void;
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

export default function TaskList({ tasks, onEdit, onDelete, onTimeUpdate }: TaskListProps) {
  const [mounted, setMounted] = useState(false);
  const [activeTimer, setActiveTimer] = useState<{
    taskId: string;
    taskName: string;
    seconds: number;
  } | null>(null);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (activeTimer && tasks.length > 0) {
      const task = tasks.find(t => t.id === activeTimer.taskId);
      if (task && task.timeSpent !== undefined && task.timeSpent !== activeTimer.seconds) {
        const diff = Math.abs(task.timeSpent - activeTimer.seconds);
        if (diff > 1) {
          setActiveTimer(prev => prev ? { ...prev, seconds: task.timeSpent || 0 } : null);
        }
      }
    }
  }, [tasks]);

  // Group tasks by category and sort by priority
  const tasksByCategory = tasks.reduce((acc, task) => {
    const category = task.category;
    if (!acc[category]) {
      acc[category] = [];
    }
    acc[category].push(task);
    return acc;
  }, {} as Record<TaskCategory, Task[]>);

  if (!mounted) {
    return <div className="space-y-8" />;
  }

  // Sort function for priorities
  const priorityOrder = { high: 0, medium: 1, low: 2 };
  const sortByPriority = (a: Task, b: Task) => {
    return priorityOrder[a.priority] - priorityOrder[b.priority];
  };

  // Sort tasks within each category
  Object.values(tasksByCategory).forEach(categoryTasks => {
    categoryTasks.sort(sortByPriority);
  });

  const getPriorityColor = (priority: Task['priority']) => {
    switch (priority) {
      case 'high': return 'text-red-600';
      case 'medium': return 'text-orange-600';
      case 'low': return 'text-green-600';
      default: return 'text-gray-600';
    }
  };

  const formatDate = (timestamp: string): string => {
    const date = new Date(timestamp);
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`;
  };

  const handleStartTimer = (task: Task) => {
    setActiveTimer({
      taskId: task.id,
      taskName: task.title,
      seconds: task.timeSpent || 0
    });
  };

  const handleStopTimer = () => {
    if (activeTimer && onTimeUpdate) {
      const currentTime = new Date().toISOString();
      
      // Get the current task
      const task = tasks.find(t => t.id === activeTimer.taskId);
      if (!task) return;

      // Create updated task with new time record
      const updatedTask = {
        ...task,
        timeSpent: activeTimer.seconds,
        timeRecords: [
          ...(task.timeRecords || []),
          {
            timestamp: currentTime,
            seconds: activeTimer.seconds
          }
        ]
      };

      // Update parent component
      onTimeUpdate(activeTimer.taskId, activeTimer.seconds, updatedTask.timeRecords);
      setActiveTimer(null);
    }
  };

  const handleTimeUpdate = (taskId: string, seconds: number) => {
    const task = tasks.find(t => t.id === taskId);
    onTimeUpdate?.(taskId, seconds, task?.timeRecords || []);
  };

  return (
    <div className="space-y-8">
      {tasks.length === 0 ? (
        <div className="text-center py-12 bg-gray-50 rounded-lg">
          <p className="text-gray-500">No tasks yet. Create your first task!</p>
        </div>
      ) : (
        Object.entries(TASK_CATEGORIES).map(([category, { name, color }]) => {
          const categoryTasks = tasksByCategory[category as TaskCategory] || [];
          if (categoryTasks.length === 0) return null;

          return (
            <div key={category} className="space-y-3">
              <h3 className={`font-medium ${color} inline-block px-3 py-1 rounded-full text-sm`}>
                {name}
              </h3>
              
              <div className="space-y-2">
                {categoryTasks.map((task) => (
                  <div
                    key={task.id}
                    className={`p-4 rounded-lg bg-opacity-50 transition-all hover:bg-opacity-70 ${
                      category === 'development' ? 'bg-blue-50' :
                      category === 'design' ? 'bg-purple-50' :
                      category === 'research' ? 'bg-green-50' :
                      category === 'meeting' ? 'bg-yellow-50' :
                      'bg-indigo-50'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="space-y-1">
                        <h4 className="font-medium text-gray-900">{task.title}</h4>
                        <p className="text-sm text-gray-600">{task.description}</p>
                        
                        <p className="text-xs text-gray-500">
                          Created: {formatDate(task.createdAt)}
                        </p>
                        
                        {task.timeRecords && task.timeRecords.length > 0 && (
                          <div className="mt-2 text-xs text-gray-500">
                            <p>Time Records:</p>
                            <div className="ml-2">
                              Stopped at: {formatDate(task.timeRecords[task.timeRecords.length - 1].timestamp)} - Duration: {Math.floor(task.timeRecords[task.timeRecords.length - 1].seconds / 60)} minutes
                            </div>
                          </div>
                        )}
                        
                        <div className="flex items-center gap-2 mt-2">
                          <span className={`inline-flex items-center gap-1 text-xs ${getPriorityColor(task.priority)}`}>
                            <Flag className="h-3 w-3" />
                            {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                          </span>
                        </div>
                      </div>

                      <div className="flex items-center gap-2">
                        <Button
                          onClick={() => {
                            onEdit(task);
                            window.scrollTo({ top: 0, behavior: 'smooth' });
                          }}
                          variant="ghost"
                          size="sm"
                          className="h-8 w-8 p-0 hover:bg-gray-100"
                        >
                          <Pencil className="h-4 w-4 text-blue-600" />
                        </Button>
                        <Button
                          onClick={() => onDelete(task.id)}
                          variant="ghost"
                          size="sm"
                          className="h-8 w-8 p-0 hover:bg-red-100"
                        >
                          <Trash2 className="h-4 w-4 text-red-600" />
                        </Button>
                      </div>
                    </div>
                    <TimeTracker 
                      taskId={task.id}
                      timeSpent={task.timeSpent || 0}
                      onTimeUpdate={(seconds) => handleTimeUpdate(task.id, seconds)}
                      onStart={() => handleStartTimer(task)}
                      isActive={activeTimer?.taskId === task.id}
                    />
                  </div>
                ))}
              </div>
            </div>
          );
        })
      )}
      {activeTimer && (
        <FloatingTimer
          seconds={activeTimer.seconds}
          taskName={activeTimer.taskName}
          onStop={handleStopTimer}
          isRunning={true}
        />
      )}
    </div>
  );
} 