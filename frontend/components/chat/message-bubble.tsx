'use client';

import { cn } from '@/lib/utils';
import { Bot, User } from 'lucide-react';

interface MessageBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
  className?: string;
}

export default function MessageBubble({ role, content, timestamp, className }: MessageBubbleProps) {
  const isUser = role === 'user';

  return (
    <div className={cn(
      "flex",
      isUser ? "justify-end" : "justify-start",
      className
    )}>
      <div
        className={cn(
          "max-w-xs lg:max-w-md px-4 py-2 rounded-lg",
          isUser
            ? "bg-primary text-primary-foreground"
            : "bg-muted"
        )}
      >
        <div className="flex items-start gap-2">
          {!isUser && <Bot className="h-4 w-4 mt-0.5 flex-shrink-0" />}
          <div className="whitespace-pre-wrap break-words">
            {content}
          </div>
          {isUser && <User className="h-4 w-4 mt-0.5 flex-shrink-0" />}
        </div>
        {timestamp && (
          <div
            className={cn(
              "text-xs mt-1",
              isUser ? "text-primary-foreground/70" : "text-muted-foreground"
            )}
          >
            {timestamp.toLocaleTimeString([], {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </div>
        )}
      </div>
    </div>
  );
}