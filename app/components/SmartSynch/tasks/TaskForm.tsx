import { useState } from "react";
import { Calendar, Clock, Flag, Folder } from 'lucide-react'
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
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(task);
  };

  return (
    <Card className="p-6 space-y-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <Input
            placeholder="Task title"
            value={task.title}
            onChange={(e) => setTask({ ...task, title: e.target.value })}
            className="text-lg font-semibold"
          />
        </div>

        <div className="space-y-2">
          <Textarea
            placeholder="Description"
            value={task.description}
            onChange={(e) => setTask({ ...task, description: e.target.value })}
            className="min-h-[100px]"
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <Select
              value={task.category}
              onValueChange={(value) => setTask({ ...task, category: value as TaskCategory })}
            >
              <SelectTrigger className="w-full">
                <Folder className="w-4 h-4 mr-2" />
                <SelectValue placeholder="Category" />
              </SelectTrigger>
              <SelectContent>
                {Object.entries(TASK_CATEGORIES).map(([key, { name }]) => (
                  <SelectItem key={`category-${key}`} value={key}>
                    {name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Select
              value={task.priority}
              onValueChange={(value) => setTask({ ...task, priority: value as Task['priority'] })}
            >
              <SelectTrigger className="w-full">
                <Flag className="w-4 h-4 mr-2" />
                <SelectValue placeholder="Priority" />
              </SelectTrigger>
              <SelectContent>
                {['low', 'medium', 'high'].map((p) => (
                  <SelectItem key={`priority-${p}`} value={p}>
                    {p.charAt(0).toUpperCase() + p.slice(1)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="space-y-2">
          <div className="flex items-center space-x-2">
            <Clock className="w-4 h-4" />
            <Input
              type="number"
              placeholder="Estimated time (minutes)"
              value={task.estimatedTime || ''}
              onChange={(e) => setTask({ ...task, estimatedTime: Number(e.target.value) })}
              className="w-full"
            />
          </div>
        </div>

        <div className="flex justify-end space-x-2">
          <Button type="submit" className="w-full">
            {isEditing ? 'Update Task' : 'Create Task'}
          </Button>
        </div>
      </form>
    </Card>
  );
}