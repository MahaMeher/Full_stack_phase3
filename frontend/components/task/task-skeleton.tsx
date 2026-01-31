import { Card } from '@/components/ui/card';

export function TaskSkeleton() {
  return (
    <div className="rounded-2xl p-6 animate-pulse glass-card border border-white/20">
      <div className="flex items-start gap-5">
        <div className="h-6 w-6 rounded-full bg-gradient-to-r from-primary-200 to-primary-300 mt-1"></div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center justify-between">
            <div className="h-5 bg-gradient-to-r from-primary-200 to-primary-300 rounded w-1/3"></div>
          </div>

          <div className="mt-3 space-y-2">
            <div className="h-4 bg-gradient-to-r from-primary-100 to-primary-200 rounded w-2/3"></div>
            <div className="h-4 bg-gradient-to-r from-primary-100 to-primary-200 rounded w-1/2"></div>
          </div>

          <div className="mt-4 flex items-center justify-between">
            <div className="h-3 bg-gradient-to-r from-primary-100 to-primary-200 rounded w-1/4"></div>
            <div className="h-3 bg-gradient-to-r from-primary-100 to-primary-200 rounded w-1/4"></div>
          </div>
        </div>

        <div className="flex gap-2">
          <div className="h-10 w-16 rounded-xl bg-gradient-to-r from-primary-100 to-primary-200"></div>
          <div className="h-10 w-16 rounded-xl bg-gradient-to-r from-primary-100 to-primary-200"></div>
        </div>
      </div>
    </div>
  );
}

export function TaskListSkeleton({ count = 6 }: { count?: number }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {Array.from({ length: count }).map((_, index) => (
        <TaskSkeleton key={index} />
      ))}
    </div>
  );
}