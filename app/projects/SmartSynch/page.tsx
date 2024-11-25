"use client";

import { useState } from "react";
import Header from "../../components/SmartSynch/layout/Header";
import TaskForm, { Task } from '../../components/SmartSynch/tasks/TaskForm';
import TaskList from '../../components/SmartSynch/tasks/TaskList';
import { Card } from "../../components/common/Card";

export default function SmartSynchPage() {
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
    <div className="min-h-screen bg-gray-50">
      <Header onNavigate={(page: string) => {}} />
      <main className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Input Form */}
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-semibold text-gray-900">Create Task</h2>
              <p className="mt-1 text-sm text-gray-500">Add a new task to your project.</p>
            </div>
            
            <Card className="bg-white p-6">
              <TaskForm 
                onSubmit={handleTaskSubmit}
                initialTask={editingTask || undefined}
                isEditing={!!editingTask}
              />
            </Card>

            {/* Help section */}
            <div className="bg-violet-50 rounded-lg p-4">
              <div className="flex items-start gap-3">
                <div className="text-violet-600">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h3 className="font-medium text-gray-900">Need help?</h3>
                  <p className="text-sm text-gray-600 mt-1">
                    Check our documentation or contact support.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Right Column - Task List */}
          <div>
            <div className="mb-6">
              <h2 className="text-2xl font-semibold text-gray-900">Your Tasks</h2>
              <p className="mt-1 text-sm text-gray-500">Manage and track your existing tasks.</p>
            </div>
            
            <Card className="bg-white p-6">
              <TaskList 
                tasks={tasks}
                onEdit={handleEditTask}
                onDelete={handleDeleteTask}
              />
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
} 