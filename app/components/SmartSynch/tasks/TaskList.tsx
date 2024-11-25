import { Task, TASK_CATEGORIES } from './TaskForm';

interface TaskListProps {
  tasks: Task[];
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
}

export default function TaskList({ tasks, onEdit, onDelete }: TaskListProps) {
  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <div
          key={task.id}
          className="bg-white dark:bg-gray-800 p-4 rounded-lg shadow space-y-2 border-l-4"
          style={{ borderLeftColor: TASK_CATEGORIES[task.category].color.split(' ')[1].replace('text', 'border') }}
        >
          <div className="flex justify-between items-start">
            <div>
              <h3 className="font-semibold text-lg">{task.title}</h3>
              <p className="text-gray-600 dark:text-gray-300">{task.description}</p>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => onEdit(task)}
                className="text-blue-600 hover:text-blue-800"
              >
                Edit
              </button>
              <button
                onClick={() => onDelete(task.id)}
                className="text-red-600 hover:text-red-800"
              >
                Delete
              </button>
            </div>
          </div>
          <div className="flex space-x-4 text-sm">
            <span className={`px-2 py-1 rounded ${
              task.priority === 'high' ? 'bg-red-100 text-red-800' :
              task.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
              'bg-green-100 text-green-800'
            }`}>
              {task.priority}
            </span>
            <span className={`px-2 py-1 rounded ${TASK_CATEGORIES[task.category].color}`}>
              {TASK_CATEGORIES[task.category].name}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
} 