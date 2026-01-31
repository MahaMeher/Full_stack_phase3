'use client';

import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface FloatingChatIconProps {
  onOpenChat: () => void;
  hasUnread?: boolean;
}

export default function FloatingChatIcon({ onOpenChat, hasUnread = false }: FloatingChatIconProps) {
  const [isHovered, setIsHovered] = useState(false);

  return (
    <AnimatePresence>
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        exit={{ scale: 0 }}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        className="fixed bottom-6 right-6 z-40"
      >
        <Button
          onClick={onOpenChat}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          className="relative h-14 w-14 rounded-full shadow-lg"
          size="icon"
        >
          <Bot className="h-6 w-6" />
          {hasUnread && (
            <span className="absolute -top-1 -right-1 h-5 w-5 rounded-full bg-red-500 flex items-center justify-center">
              <span className="h-2 w-2 rounded-full bg-white"></span>
            </span>
          )}
        </Button>

        {/* Tooltip */}
        <AnimatePresence>
          {isHovered && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 10 }}
              className="absolute bottom-full right-0 mb-2 px-2 py-1 bg-gray-800 text-white text-xs rounded-md whitespace-nowrap"
            >
              Open AI Assistant
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </AnimatePresence>
  );
}