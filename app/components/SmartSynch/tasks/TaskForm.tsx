import { useState } from "react";
import { Calendar, Clock, Flag, Folder, Search, X } from 'lucide-react'
import { Button } from "../../common/Button"
import { Card } from "../../common/Card"
import { Input } from "../../common/Input"
import { Textarea } from "../../common/Textarea"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../../common/Select"

interface TaskFormProps {
  onSubmit: (task: Task) => void;
  initialTask?: Task;
  isEditing?: boolean;
}

export const TASK_CATEGORIES = {
  'development': { name: 'Development', color: 'bg-blue-100 text-blue-800' },
  'design': { name: 'Design', color: 'bg-purple-100 text-purple-800' },
  'research': { name: 'Research', color: 'bg-green-100 text-green-800' },
  'meeting': { name: 'Meeting', color: 'bg-yellow-100 text-yellow-800' },
  'planning': { name: 'Planning', color: 'bg-indigo-100 text-indigo-800' },
} as const;

export type TaskCategory = keyof typeof TASK_CATEGORIES;

export interface Task {
  id: string;
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  category: TaskCategory;
  estimatedTime?: number;
}

export default function TaskForm({ onSubmit, initialTask, isEditing = false }: TaskFormProps) {
  const [task, setTask] = useState<Task>(initialTask || {
    id: crypto.randomUUID(),
    title: '',
    description: '',
    priority: 'medium',
    category: 'development',
    estimatedTime: undefined
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(task);
    if (!isEditing) {
      resetForm();
    }
  };

  const resetForm = () => {
    setTask({
      id: crypto.randomUUID(),
      title: '',
      description: '',
      priority: 'medium',
      category: 'development',
      estimatedTime: undefined
    });
  };

  const getPriorityLabel = (priority: string) => {
    const labels = {
      low: 'Low Priority',
      medium: 'Medium Priority',
      high: 'High Priority'
    };
    return labels[priority as keyof typeof labels] || priority;
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Task Title <span className="text-red-500">*</span>
          </label>
          <div className="relative">
            <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none">
              <Search className="h-4 w-4 text-gray-400" />
            </div>
            <Input
              type="text"
              value={task.title}
              onChange={(e) => setTask({ ...task, title: e.target.value })}
              className="pl-10 pr-10 w-full bg-white text-gray-900"
              placeholder="Enter task title"
              required
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Description <span className="text-red-500">*</span>
          </label>
          <Textarea
            value={task.description}
            onChange={(e) => setTask({ ...task, description: e.target.value })}
            className="w-full bg-white text-gray-900"
            placeholder="Enter task description"
            required
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Priority <span className="text-red-500">*</span>
            </label>
            <Select
              value={task.priority}
              onValueChange={(value: 'low' | 'medium' | 'high') => 
                setTask({ ...task, priority: value })
              }
            >
              <SelectTrigger className="w-full bg-white text-gray-900">
                <div className="flex items-center gap-2">
                  <Flag className={`h-4 w-4 ${
                    task.priority === 'high' ? 'text-red-500' :
                    task.priority === 'medium' ? 'text-orange-500' :
                    'text-green-500'
                  }`} />
                  <span className="text-gray-900">{getPriorityLabel(task.priority)}</span>
                </div>
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="low" className="text-gray-900">Low Priority</SelectItem>
                <SelectItem value="medium" className="text-gray-900">Medium Priority</SelectItem>
                <SelectItem value="high" className="text-gray-900">High Priority</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Category <span className="text-red-500">*</span>
            </label>
            <Select
              value={task.category}
              onValueChange={(value: TaskCategory) => 
                setTask({ ...task, category: value })
              }
            >
              <SelectTrigger className="w-full bg-white text-gray-900">
                <div className="flex items-center gap-2">
                  <Folder className="h-4 w-4" />
                  <span className="text-gray-900">{TASK_CATEGORIES[task.category].name}</span>
                </div>
              </SelectTrigger>
              <SelectContent>
                {Object.entries(TASK_CATEGORIES).map(([key, { name }]) => (
                  <SelectItem key={key} value={key} className="text-gray-900">
                    {name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>
      </div>

      <div className="flex gap-3 pt-4">
        <Button
          type="submit"
          className="bg-violet-600 hover:bg-violet-700 text-white"
        >
          {isEditing ? 'Update Task' : 'Create Task'}
        </Button>
        <Button
          type="button"
          variant="outline"
          onClick={resetForm}
          className="bg-red-600 hover:bg-red-700 text-white border-red-600 hover:border-red-700"
        >
          Clear Form
        </Button>
      </div>
    </form>
  );
}