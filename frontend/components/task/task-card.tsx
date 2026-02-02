'use client';

import { useState, memo } from 'react';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Task } from '@/types/task';
import { formatDate } from '@/lib/utils';

interface TaskCardProps {
  task: Task;
  onToggleComplete: (id: string) => void;
  onEdit: (task: Task) => void;
  onDelete: (id: string) => void;
}

const TaskCardComponent = ({ task, onToggleComplete, onEdit, onDelete }: TaskCardProps) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleComplete = () => {
    onToggleComplete(task.id);
  };

  const handleEdit = () => {
    onEdit(task);
  };

  const handleDelete = () => {
    onDelete(task.id);
  };

  return (
    <div className={`rounded-2xl p-6 transition-all duration-500 ease-out transform hover:scale-[1.02] glass-card border border-white/20 animate-fade-in-up ${
      task.completed ? 'opacity-80 grayscale' : ''
    }`} style={{ animationDelay: `${Math.random() * 200}ms` }}>
      <div className="flex items-start gap-5">
        <div className="relative mt-1">
          <Checkbox
            checked={task.completed}
            onCheckedChange={toggleComplete}
            className="h-6 w-6 rounded-full border-2 transition-all duration-300 data-[state=checked]:bg-gradient-purple-pink data-[state=checked]:border-transparent data-[state=checked]:scale-110 hover:scale-105"
          />
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <h3 className={`text-xl font-bold transition-all duration-300 ${
              task.completed
                ? 'line-through text-muted-foreground/70'
                : 'text-foreground'
            }`}>
              {task.title}
            </h3>
          </div>

          {task.description && (
            <p className={`mt-3 text-base transition-all duration-300 ${
              task.completed ? 'text-muted-foreground/70' : 'text-muted-foreground'
            } hover:scale-[1.01]`}>
              {task.description}
            </p>
          )}

          <div className={`mt-4 flex items-center justify-between text-sm transition-all duration-300 ${
            task.completed ? 'text-muted-foreground/60' : 'text-muted-foreground/80'
          }`}>
            <span className="flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Created: {formatDate(task.createdAt)}
            </span>
            <span className="flex items-center gap-2">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Updated: {formatDate(task.updatedAt)}
            </span>
          </div>
        </div>

        <div className="flex gap-2 transition-all duration-300 hover:scale-105">
          <Button
            variant="outline"
            size="sm"
            onClick={handleEdit}
            className="transition-all duration-300 hover:scale-105 text-sm font-medium hover:shadow-lg"
            aria-label="Edit task"
          >
            Edit
          </Button>
          <Button
            variant="destructive"
            size="sm"
            onClick={handleDelete}
            className="transition-all duration-300 hover:scale-105 text-sm font-medium hover:shadow-lg"
            aria-label="Delete task"
          >
            Delete
          </Button>
        </div>
      </div>
    </div>
  );
};

export const TaskCard = memo(TaskCardComponent);