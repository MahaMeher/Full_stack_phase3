'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/use-auth';
import { useTask } from '@/hooks/use-task';
import { Button } from '@/components/ui/button';
import { TaskCard } from '@/components/task/task-card';
import { TaskModal } from '@/components/task/task-modal';
import { TaskListSkeleton } from '@/components/task/task-skeleton';
import { TaskEmptyState } from '@/components/task/task-empty-state';
import { useThemeContext } from '@/components/theme/provider';
import { ThemeToggle } from '@/components/theme/toggle';
import ChatPanel from '@/components/chat/chat-panel';
import { Plus, Calendar, CheckCircle, Clock } from 'lucide-react';

export default function DashboardPage() {
  const router = useRouter();
  const { user, logout } = useAuth();
  const { tasks, loading, error, createTask, updateTask, deleteTask, toggleTaskCompletion } = useTask();
  const { theme, toggleTheme } = useThemeContext();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<any>(null);

  const handleLogout = async () => {
    await logout();
    router.push('/sign-in'); // Redirect to login page after logout
  };

  const handleAddTask = () => {
    setEditingTask(null);
    setIsModalOpen(true);
  };

  const handleEditTask = (task: any) => {
    setEditingTask(task);
    setIsModalOpen(true);
  };

  const handleSaveTask = async (taskData: any) => {
    let result;

    if (editingTask) {
      result = await updateTask(editingTask.id, taskData);
    } else {
      result = await createTask(taskData);
    }

    if (result.success) {
      setIsModalOpen(false);
      setEditingTask(null);
    }
  };

  const handleDeleteTask = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      await deleteTask(id);
    }
  };

  const handleToggleTask = async (id: string) => {
    await toggleTaskCompletion(id);
  };

  const completedTasks = tasks.filter(task => task.completed).length;
  const pendingTasks = tasks.length - completedTasks;

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50/50 via-accent-50/30 to-secondary-50/50 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6 mb-10">
          <div className="space-y-3">
            <h1 className="text-4xl font-bold text-foreground">
              Welcome, {user?.name || user?.email || 'User'}!
            </h1>
            <p className="text-muted-foreground/80 text-lg">
              Manage your tasks efficiently and boost productivity
            </p>

            <div className="flex flex-wrap gap-4 mt-4">
              <div className="flex items-center gap-2 bg-white/50 dark:bg-white/10 backdrop-blur-sm rounded-xl px-4 py-3 border border-white/20">
                <Calendar className="h-5 w-5 text-primary-600" />
                <div>
                  <p className="text-sm text-muted-foreground/70">Total Tasks</p>
                  <p className="text-xl font-bold text-foreground">{tasks.length}</p>
                </div>
              </div>

              <div className="flex items-center gap-2 bg-white/50 dark:bg-white/10 backdrop-blur-sm rounded-xl px-4 py-3 border border-white/20">
                <CheckCircle className="h-5 w-5 text-success-600" />
                <div>
                  <p className="text-sm text-muted-foreground/70">Completed</p>
                  <p className="text-xl font-bold text-success-600">{completedTasks}</p>
                </div>
              </div>

              <div className="flex items-center gap-2 bg-white/50 dark:bg-white/10 backdrop-blur-sm rounded-xl px-4 py-3 border border-white/20">
                <Clock className="h-5 w-5 text-warning-600" />
                <div>
                  <p className="text-sm text-muted-foreground/70">Pending</p>
                  <p className="text-xl font-bold text-warning-600">{pendingTasks}</p>
                </div>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <ThemeToggle />
            <Button onClick={handleAddTask} variant="gradient" size="lg" className="gap-2">
              <Plus className="h-5 w-5" /> Add Task
            </Button>
            <Button onClick={handleLogout} variant="outline" className="border-white/30">
              Logout
            </Button>
          </div>
        </div>

        {error && (
          <div className="mb-6 p-4 bg-destructive/20 border border-destructive/30 rounded-2xl text-destructive backdrop-blur-sm">
            <div className="flex items-center gap-2">
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Error: {error}</span>
            </div>
          </div>
        )}

        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <TaskListSkeleton count={6} />
          </div>
        ) : tasks.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="text-center space-y-6 max-w-md">
              <div className="w-24 h-24 bg-gradient-purple-pink rounded-full flex items-center justify-center mx-auto">
                <Calendar className="h-12 w-12 text-white" />
              </div>
              <div>
                <h3 className="text-2xl font-bold text-foreground mb-2">No tasks yet</h3>
                <p className="text-muted-foreground/80 mb-6">
                  Get started by creating your first task to organize your day
                </p>
                <Button onClick={handleAddTask} variant="gradient" size="lg" className="gap-2">
                  <Plus className="h-5 w-5" /> Create Your First Task
                </Button>
              </div>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {tasks.map(task => (
              <TaskCard
                key={task.id}
                task={task}
                onToggleComplete={handleToggleTask}
                onEdit={handleEditTask}
                onDelete={handleDeleteTask}
              />
            ))}
          </div>
        )}

        <TaskModal
          isOpen={isModalOpen}
          onClose={() => {
            setIsModalOpen(false);
            setEditingTask(null);
          }}
          task={editingTask}
          onSave={handleSaveTask}
        />

        {/* AI Chat Panel */}
        <ChatPanel />
      </div>
    </div>
  );
}