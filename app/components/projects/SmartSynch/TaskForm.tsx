import { useState, useEffect } from 'react';
import { Input } from '../../../components/common/Input';
import { Textarea } from '../../../components/common/Textarea';
import { Button } from '../../../components/common/Button';
import { Search, Flag, Folder } from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
} from "../../../components/common/Select"
import { predictTaskCategory } from '../../../projects/SmartSynch/api/taskPredictor';
import { debounce } from 'lodash';
import { submitTaskFeedback } from '../../../projects/SmartSynch/api/taskFeedback';
import { TASK_CATEGORIES, TaskCategory } from '../../../lib/categories';

interface TaskFormProps {
  onSubmit: (task: Task) => void;
  initialTask?: Task;
  isEditing?: boolean;
}

export interface Task {
  id: string;
  title: string;
  description: string;
  category: TaskCategory;
  priority: 'high' | 'medium' | 'low';
  timeSpent?: number;
  createdAt: string;
  timeRecords: {
    timestamp: string;
    seconds: number;
  }[];
}

function getCategoryFromId(id: number): TaskCategory {
  const categories = Object.keys(TASK_CATEGORIES) as TaskCategory[];
  return categories[id] || 'other'; // fallback to 'other' if invalid id
}

export default function TaskForm({ onSubmit, initialTask, isEditing = false }: TaskFormProps) {
  const [task, setTask] = useState<Task>({
    id: crypto.randomUUID(),
    title: '',
    description: '',
    priority: 'medium',
    category: 'development',
    timeSpent: undefined,
    createdAt: new Date().toISOString(),
    timeRecords: []
  });

  const [prediction, setPrediction] = useState<{
    category: TaskCategory | null;
    confidence: number;
  }>({ category: null, confidence: 0 });

  useEffect(() => {
    if (initialTask) {
      setTask(initialTask);
    }
  }, [initialTask]);

  useEffect(() => {
    const getPrediction = debounce(async () => {
      if (task.title.length > 3 && task.description.length > 10) {
        try {
          // Predict the task category
          const result = await predictTaskCategory(task.title, task.description);
          if (result.confidence > 0.7) {
            const categoryId = typeof result.category === 'number' ? result.category : parseInt(result.category, 10);
            setPrediction({
              category: getCategoryFromId(categoryId),
              confidence: result.confidence
            });
            setTask(prev => ({ ...prev, category: getCategoryFromId(categoryId) }));
          }
        } catch (error: any) {
          console.error('Prediction failed:', error);
          console.error('Error details:', error.message);
          console.error('Full error object:', error);
        }
      }
    }, 500);

    getPrediction();
    return () => getPrediction.cancel();
  }, [task.title, task.description]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Submit feedback if we had a prediction
    if (prediction.category) {
      await submitTaskFeedback(
        task.title,
        task.description,
        prediction.category,
        task.category,
        prediction.category === task.category
      );
    }
    
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
      timeSpent: undefined,
      createdAt: new Date().toISOString(),
      timeRecords: []
    });
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
                  <span className="text-gray-900">{task.priority?.charAt(0).toUpperCase() + task.priority?.slice(1)} Priority</span>
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
                <div className="flex items-center justify-between w-full">
                  <div className="flex items-center gap-2">
                    <Folder className="h-4 w-4" />
                    <span className="text-gray-900">{TASK_CATEGORIES[task.category]?.name}</span>
                  </div>
                  {prediction.confidence > 0.7 && (
                    <span className="text-xs text-green-600">
                      {Math.round(prediction.confidence * 100)}% match
                    </span>
                  )}
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