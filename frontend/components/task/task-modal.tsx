'use client';

import { useState, useEffect, useCallback } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Task, TaskFormData } from '@/types/task';
import { taskSchema } from '@/lib/validations';

interface TaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  task?: Task | null;
  onSave: (taskData: TaskFormData) => void;
  isSubmitting?: boolean;
}

export function TaskModal({ isOpen, onClose, task, onSave, isSubmitting = false }: TaskModalProps) {
  const [formData, setFormData] = useState<TaskFormData>({ title: '', description: '' });
  const [errors, setErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title,
        description: task.description || '',
      });
    } else {
      setFormData({ title: '', description: '' });
    }
    setErrors({});
  }, [task, isOpen]);

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user types
    if (errors[name]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  }, [errors]);

  const handleSubmit = useCallback((e: React.FormEvent) => {
    e.preventDefault();

    // Clear previous errors
    setErrors({});

    // Validate input
    try {
      taskSchema.parse(formData);

      // Call onSave prop
      onSave(formData);
    } catch (validationError: any) {
      const fieldErrors: Record<string, string> = {};
      if (validationError.errors) {
        validationError.errors.forEach((error: any) => {
          fieldErrors[error.path[0]] = error.message;
        });
      }
      setErrors(fieldErrors);
    }
  }, [formData, onSave]);

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-lg rounded-2xl glass-card border-white/30 backdrop-blur-xl bg-white/10 dark:bg-black/20 p-0 max-w-md" aria-describedby={undefined}>
        <DialogHeader className="px-6 pt-6 pb-4">
          <DialogTitle className="text-2xl font-bold bg-gradient-purple-pink bg-clip-text text-transparent">
            {task ? 'Edit Task' : 'Add New Task'}
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6 px-6 pb-6" noValidate>
          <div className="space-y-3">
            <label htmlFor="title" className="text-sm font-semibold text-foreground/90">
              Title *
            </label>
            <Input
              id="title"
              name="title"
              value={formData.title}
              onChange={handleChange}
              placeholder="Task title"
              className={`${errors.title ? 'border-red-500' : 'border-white/30'} h-12 text-base`}
              aria-invalid={!!errors.title}
              aria-describedby={errors.title ? "title-error" : undefined}
              required
            />
            {errors.title && (
              <p id="title-error" className="text-red-400 text-sm" role="alert">{errors.title}</p>
            )}
          </div>

          <div className="space-y-3">
            <label htmlFor="description" className="text-sm font-semibold text-foreground/90">
              Description
            </label>
            <Textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Task description (optional)"
              rows={4}
              className="border-white/30 text-base min-h-[120px]"
              aria-describedby={errors.description ? "description-error" : undefined}
            />
            {errors.description && (
              <p id="description-error" className="text-red-400 text-sm" role="alert">{errors.description}</p>
            )}
          </div>

          <div className="flex justify-end space-x-3 pt-2">
            <Button
              type="button"
              variant="outline"
              onClick={onClose}
              className="h-11 px-5 text-base font-medium"
              aria-label="Cancel"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="gradient"
              disabled={isSubmitting}
              className="h-11 px-6 text-base font-bold"
              aria-busy={isSubmitting}
            >
              {isSubmitting
                ? (task ? 'Updating...' : 'Creating...')
                : (task ? 'Update Task' : 'Create Task')
              }
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
}