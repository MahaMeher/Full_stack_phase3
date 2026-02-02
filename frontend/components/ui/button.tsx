import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';

import { cn } from '@/lib/utils';

const buttonVariants = cva(
  'inline-flex items-center justify-center whitespace-nowrap rounded-xl text-sm font-semibold ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 active:scale-[0.96] transition-all duration-300 ease-out group relative overflow-hidden',
  {
    variants: {
      variant: {
        default: 'bg-gradient-purple-pink text-primary-foreground shadow-lg hover:shadow-xl hover:scale-[1.02] hover:shadow-primary-500/25',
        destructive: 'bg-gradient-to-r from-error-500 to-error-600 text-error-foreground shadow-lg hover:shadow-xl hover:scale-[1.02] hover:shadow-error-500/25',
        outline: 'border border-primary-300 bg-white/90 text-primary-700 hover:bg-primary-100/90 backdrop-blur-sm shadow-sm hover:shadow-md dark:border-primary-600 dark:bg-gray-800/90 dark:text-primary-100 dark:hover:bg-gray-700/90',
        secondary: 'bg-gradient-to-r from-secondary-400 to-secondary-500 text-secondary-foreground shadow-sm hover:shadow-md hover:scale-[1.02] dark:from-secondary-600 dark:to-secondary-700',
        ghost: 'hover:bg-primary-100/50 text-primary-700 hover:text-primary-900 backdrop-blur-sm dark:hover:bg-primary-800/30 dark:text-primary-300 dark:hover:text-primary-100',
        link: 'text-primary-600 underline-offset-4 hover:underline hover:text-primary-700',
        success: 'bg-gradient-to-r from-success-500 to-success-600 text-success-foreground shadow-sm hover:shadow-md hover:scale-[1.02]',
        warning: 'bg-gradient-to-r from-warning-500 to-warning-600 text-warning-foreground shadow-sm hover:shadow-md hover:scale-[1.02]',
        accent: 'bg-gradient-to-r from-accent-500 to-accent-600 text-accent-foreground shadow-sm hover:shadow-md hover:scale-[1.02] dark:from-accent-600 dark:to-accent-700',
        glass: 'bg-white/10 backdrop-blur-lg border border-white/20 text-white shadow-lg hover:shadow-xl hover:scale-[1.02] hover:bg-white/20',
        gradient: 'bg-gradient-rainbow text-white shadow-lg hover:shadow-xl hover:scale-[1.02] hover:shadow-primary-500/25',
      },
      size: {
        default: 'h-11 px-5 py-2.5',
        sm: 'h-9 px-3.5 py-2 text-xs',
        lg: 'h-13 px-7 text-base font-bold',
        xl: 'h-16 px-9 text-lg font-bold',
        icon: 'h-11 w-11',
        'icon-sm': 'h-9 w-9',
        'icon-lg': 'h-14 w-14',
      },
      rounded: {
        default: 'rounded-xl',
        full: 'rounded-full',
        none: 'rounded-none',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
      rounded: 'default',
    },
  }
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, rounded, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : 'button';
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, rounded, className }))}
        ref={ref}
        {...props}
      />
    );
  }
);
Button.displayName = 'Button';

export { Button, buttonVariants };