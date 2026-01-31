'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Send, X, Bot, User } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import { getSession } from '@/lib/auth';
import { apiClient } from '@/lib/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatWindowProps {
  isOpen: boolean;
  onClose: () => void;
  conversationId?: string;
}

export default function ChatWindow({ isOpen, onClose, conversationId }: ChatWindowProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  // Load conversation history if conversationId is provided
  useEffect(() => {
    if (conversationId && isOpen) {
      loadConversationHistory();
    } else {
      // Reset messages when opening a new chat
      setMessages([]);
    }
  }, [conversationId, isOpen]);

  const loadConversationHistory = async () => {
    try {
      const response = await apiClient.getConversationHistory(conversationId);

      if (!response.success) {
        throw new Error(response.error || 'Failed to load conversation history');
      }

      const data = response.data;
      const formattedMessages: Message[] = data.messages.map((msg: any) => ({
        id: msg.id,
        role: msg.role,
        content: msg.content,
        timestamp: new Date(msg.timestamp),
      }));

      setMessages(formattedMessages);
    } catch (error) {
      console.error('Error loading conversation history:', error);
      toast({
        title: 'Error',
        description: 'Failed to load conversation history',
        variant: 'destructive',
      });
    }
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    // Add user message to UI immediately
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await apiClient.sendMessage(inputValue, conversationId);

      if (!response.success) {
        throw new Error(response.error || 'Failed to get response from chat API');
      }

      const data = response.data;

      const aiMessage: Message = {
        id: `ai-${Date.now()}`,
        role: 'assistant',
        content: data.response,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);

      // Update conversation ID if it changed
      if (data.conversation_id && data.conversation_id !== conversationId) {
        // We could update the conversationId prop here if needed
      }
    } catch (error) {
      console.error('Error sending message:', error);
      toast({
        title: 'Error',
        description: 'Failed to send message. Please try again.',
        variant: 'destructive',
      });

      // Add error message to indicate failure
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: "Sorry, I encountered an error processing your request. Please try again.",
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    if (scrollAreaRef.current) {
      const scrollElement = scrollAreaRef.current.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollElement) {
        scrollElement.scrollTop = scrollElement.scrollHeight;
      }
    }
  }, [messages]);

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="bg-white rounded-lg shadow-xl w-full max-w-2xl h-[600px] flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            <Card className="flex flex-col h-full border-0 rounded-lg shadow-none">
              <CardHeader className="flex flex-row items-center justify-between p-4 border-b">
                <CardTitle className="text-lg flex items-center gap-2">
                  <Bot className="h-5 w-5 text-primary" />
                  AI Task Assistant
                </CardTitle>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={onClose}
                  className="h-8 w-8 p-0"
                >
                  <X className="h-4 w-4" />
                </Button>
              </CardHeader>

              <CardContent className="flex-1 flex flex-col p-0">
                <div
                  className="flex-1 p-4 overflow-y-auto max-h-[300px]"
                  ref={scrollAreaRef}
                >
                  <div className="space-y-4">
                    {messages.length === 0 ? (
                      <div className="text-center text-muted-foreground mt-8">
                        <Bot className="h-12 w-12 mx-auto mb-3 text-primary" />
                        <p>Hello! I'm your AI task assistant.</p>
                        <p className="text-sm">Ask me to add, list, update, or complete tasks.</p>
                      </div>
                    ) : (
                      messages.map((message) => (
                        <div
                          key={message.id}
                          className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                          <div
                            className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                              message.role === 'user'
                                ? 'bg-primary text-primary-foreground'
                                : 'bg-muted'
                            }`}
                          >
                            <div className="flex items-start gap-2">
                              {message.role === 'assistant' && (
                                <Bot className="h-4 w-4 mt-0.5 flex-shrink-0" />
                              )}
                              <div className="whitespace-pre-wrap break-words">
                                {message.content}
                              </div>
                              {message.role === 'user' && (
                                <User className="h-4 w-4 mt-0.5 flex-shrink-0" />
                              )}
                            </div>
                            <div
                              className={`text-xs mt-1 ${
                                message.role === 'user' ? 'text-primary-foreground/70' : 'text-muted-foreground'
                              }`}
                            >
                              {message.timestamp.toLocaleTimeString([], {
                                hour: '2-digit',
                                minute: '2-digit',
                              })}
                            </div>
                          </div>
                        </div>
                      ))
                    )}

                    {isLoading && (
                      <div className="flex justify-start">
                        <div className="max-w-xs lg:max-w-md px-4 py-2 rounded-lg bg-muted">
                          <div className="flex items-center gap-2">
                            <Bot className="h-4 w-4 mt-0.5" />
                            <div className="flex space-x-1">
                              <div className="h-2 w-2 bg-muted-foreground rounded-full animate-bounce"></div>
                              <div className="h-2 w-2 bg-muted-foreground rounded-full animate-bounce delay-75"></div>
                              <div className="h-2 w-2 bg-muted-foreground rounded-full animate-bounce delay-150"></div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                <div className="p-4 border-t">
                  <div className="flex gap-2">
                    <Input
                      value={inputValue}
                      onChange={(e) => setInputValue(e.target.value)}
                      onKeyDown={handleKeyDown}
                      placeholder="Ask me to add, list, or manage your tasks..."
                      disabled={isLoading}
                      className="flex-1"
                    />
                    <Button
                      onClick={sendMessage}
                      disabled={!inputValue.trim() || isLoading}
                      className="h-10"
                    >
                      <Send className="h-4 w-4" />
                    </Button>
                  </div>
                  <p className="text-xs text-muted-foreground mt-2 text-center">
                    AI assistant can help manage your tasks using natural language
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}