import { Task, TASK_CATEGORIES, TaskCategory } from './TaskForm';
import { Button } from '../../../components/common/Button';
import { Pencil, Trash2, Flag } from 'lucide-react';
import { TimeTracker } from './TimeTracker';
import { useEffect } from 'react';

interface TaskListProps {
  tasks: Task[];
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onTimeUpdate?: (taskId: string, seconds: number) => void;
}

export default function TaskList({ tasks, onEdit, onDelete, onTimeUpdate }: TaskListProps) {
  useEffect(() => {
    const storedTasks = localStorage.getItem('tasks');
    if (storedTasks) {
      const parsedTasks = JSON.parse(storedTasks);
      // You'll need to handle this in the parent component
      // setTasks(parsedTasks);
    }
  }, []);

  useEffect(() => {
    localStorage.setItem('tasks', JSON.stringify(tasks));
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

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-50 rounded-lg">
        <p className="text-gray-500">No tasks yet. Create your first task!</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {Object.entries(TASK_CATEGORIES).map(([category, { name, color }]) => {
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
                    initialTime={task.timeSpent || 0}
                    onTimeUpdate={(seconds) => {
                      onTimeUpdate?.(task.id, seconds);
                    }}
                  />
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
} 