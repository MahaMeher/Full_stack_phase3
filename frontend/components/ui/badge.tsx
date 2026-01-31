import * as React from 'react';
import { cva, type VariantProps } from 'class-variance-authority';

import { cn } from '@/lib/utils';

const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-3 py-1 text-xs font-bold transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 shadow-sm backdrop-blur-sm',
  {
    variants: {
      variant: {
        default: 'border-transparent bg-gradient-purple-pink text-primary-foreground',
        secondary: 'border-white/30 bg-white/20 text-secondary-foreground backdrop-blur-sm',
        destructive: 'border-transparent bg-gradient-to-r from-error-500 to-error-600 text-error-foreground',
        outline: 'border-primary-300 text-foreground bg-transparent',
        success: 'border-transparent bg-gradient-to-r from-success-500 to-success-600 text-success-foreground',
        warning: 'border-transparent bg-gradient-to-r from-warning-500 to-warning-600 text-warning-foreground',
        accent: 'border-transparent bg-gradient-to-r from-accent-500 to-accent-600 text-accent-foreground',
        glass: 'border-white/30 bg-white/10 text-white backdrop-blur-lg',
      },
      size: {
        default: 'h-6 px-2.5 py-0.5 text-xs',
        sm: 'h-5 px-2 py-0.25 text-xs',
        lg: 'h-8 px-3.5 py-1 text-sm',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, size, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant, size }), className)} {...props} />
  );
}

export { Badge, badgeVariants };