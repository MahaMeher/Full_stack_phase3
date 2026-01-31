'use client';

import { useState } from 'react';
import ChatWindow from './chat-window';
import FloatingChatIcon from './floating-chat-icon';

export default function ChatPanel() {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [hasUnread, setHasUnread] = useState(false);

  const handleOpenChat = () => {
    setIsChatOpen(true);
    setHasUnread(false);
  };

  const handleCloseChat = () => {
    setIsChatOpen(false);
  };

  return (
    <>
      <FloatingChatIcon
        onOpenChat={handleOpenChat}
        hasUnread={hasUnread}
      />
      <ChatWindow
        isOpen={isChatOpen}
        onClose={handleCloseChat}
      />
    </>
  );
}