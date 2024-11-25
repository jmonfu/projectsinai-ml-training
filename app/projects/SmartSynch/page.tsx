"use client";

import { useState } from "react";
import Header from "../../components/SmartSynch/layout/Header";
import TaskForm, { Task } from '../../components/SmartSynch/tasks/TaskForm';
import TaskList from '../../components/SmartSynch/tasks/TaskList';

export default function SmartSynchPage() {
  const [currentPage, setCurrentPage] = useState("new");
  const [tasks, setTasks] = useState<Task[]>([]);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  const handleTaskSubmit = (task: Task) => {
    if (editingTask) {
      setTasks(tasks.map(t => t.id === task.id ? task : t));
      setEditingTask(null);
    } else {
      setTasks([...tasks, task]);
    }
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
  };

  const handleDeleteTask = (taskId: string) => {
    setTasks(tasks.filter(task => task.id !== taskId));
  };

  return (
    <div className="h-screen flex flex-col bg-gray-100 max-w-7xl mx-auto shadow-xl">
      <Header onNavigate={setCurrentPage} />
      <main className="flex-1 p-6 overflow-y-auto">
        {currentPage === "new" && (
          <div className="flex gap-6">
            {/* Left side - Form */}
            <div className="w-1/3 bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h1 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                {editingTask ? 'Edit Task' : 'Create New Task'}
              </h1>
              <TaskForm 
                onSubmit={handleTaskSubmit}
                initialTask={editingTask || undefined}
                isEditing={!!editingTask}
              />
            </div>

            {/* Right side - Task List */}
            <div className="w-2/3 bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Tasks
              </h2>
              <TaskList 
                tasks={tasks}
                onEdit={handleEditTask}
                onDelete={handleDeleteTask}
              />
            </div>
          </div>
        )}
      </main>
    </div>
  );
} 