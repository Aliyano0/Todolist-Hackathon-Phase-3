"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MessageCircle, X, Maximize2, Send, Loader2, Info } from "lucide-react";
import { useAuth } from "@/providers/AuthProvider";
import { useRouter } from "next/navigation";
import { sendChatMessage, ChatApiError } from "@/lib/chatApi";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

const STORAGE_KEY_PREFIX = "chat_widget_";

export function ChatWidget() {
  const { user, isAuthenticated } = useAuth();
  const router = useRouter();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showInfo, setShowInfo] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load chat history from localStorage on mount
  useEffect(() => {
    if (user?.id) {
      const savedMessages = localStorage.getItem(`${STORAGE_KEY_PREFIX}messages_${user.id}`);
      const savedConversationId = localStorage.getItem(`${STORAGE_KEY_PREFIX}conversation_${user.id}`);

      if (savedMessages) {
        try {
          setMessages(JSON.parse(savedMessages));
        } catch (e) {
          console.error("Failed to load chat history:", e);
        }
      }

      if (savedConversationId) {
        setConversationId(savedConversationId);
      }
    }
  }, [user?.id]);

  // Save chat history to localStorage whenever messages or conversationId change
  useEffect(() => {
    if (user?.id && messages.length > 0) {
      localStorage.setItem(`${STORAGE_KEY_PREFIX}messages_${user.id}`, JSON.stringify(messages));
    }
  }, [messages, user?.id]);

  useEffect(() => {
    if (user?.id && conversationId) {
      localStorage.setItem(`${STORAGE_KEY_PREFIX}conversation_${user.id}`, conversationId);
    }
  }, [conversationId, user?.id]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isOpen]);

  // Don't show widget if not authenticated
  if (!isAuthenticated || !user) {
    return null;
  }

  // Don't show widget if email not verified
  if (!user.email_verified) {
    return null;
  }

  const handleSendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    setError(null);

    // Add user message to UI immediately
    const userMessageObj: Message = {
      role: "user",
      content: userMessage,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, userMessageObj]);

    setIsLoading(true);

    try {
      const response = await sendChatMessage(user.id, userMessage, conversationId);

      // Save conversation ID for subsequent messages
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant response to UI
      const assistantMessage: Message = {
        role: "assistant",
        content: response.message,
        timestamp: response.timestamp,
      };
      setMessages((prev) => [...prev, assistantMessage]);

      // Emit event for real-time task updates
      window.dispatchEvent(new CustomEvent("taskUpdated"));
    } catch (err) {
      if (err instanceof ChatApiError) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred. Please try again.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleExpandToFullChat = () => {
    router.push("/chat");
  };

  return (
    <>
      {/* Chat Widget Button */}
      <AnimatePresence>
        {!isOpen && (
          <motion.button
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0, opacity: 0 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => setIsOpen(true)}
            className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-primary text-primary-foreground rounded-full shadow-lg hover:shadow-xl transition-shadow flex items-center justify-center"
            aria-label="Open chat"
          >
            <MessageCircle className="w-6 h-6" />
          </motion.button>
        )}
      </AnimatePresence>

      {/* Chat Widget Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            className="fixed bottom-6 right-6 z-50 w-96 h-[500px] bg-card border border-border rounded-lg shadow-2xl flex flex-col overflow-hidden"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-4 border-b border-border bg-muted/50">
              <div className="flex items-center space-x-2">
                <MessageCircle className="w-5 h-5 text-primary" />
                <h3 className="font-semibold text-foreground">AI Assistant</h3>
                <button
                  onClick={() => setShowInfo(!showInfo)}
                  className="p-1 hover:bg-muted rounded-md transition-colors"
                  aria-label="Show command guide"
                >
                  <Info className="w-4 h-4 text-muted-foreground" />
                </button>
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={handleExpandToFullChat}
                  className="p-1.5 hover:bg-muted rounded-md transition-colors"
                  aria-label="Expand to full chat"
                >
                  <Maximize2 className="w-4 h-4 text-muted-foreground" />
                </button>
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-1.5 hover:bg-muted rounded-md transition-colors"
                  aria-label="Close chat"
                >
                  <X className="w-4 h-4 text-muted-foreground" />
                </button>
              </div>
            </div>

            {/* Info Panel */}
            {showInfo && (
              <div className="bg-muted/30 border-b border-border p-3 text-xs space-y-2">
                <div>
                  <p className="font-semibold text-foreground mb-1">Commands:</p>
                  <ul className="space-y-0.5 text-muted-foreground">
                    <li>• "Add task: [title]" - Create new task</li>
                    <li>• "List my tasks" - Show all tasks</li>
                    <li>• "Complete task #[number]" - Mark complete</li>
                    <li>• "Delete task #[number]" - Remove task</li>
                    <li>• "Update task #[number] title to [new title]"</li>
                  </ul>
                </div>
                <div>
                  <p className="font-semibold text-foreground mb-1">Languages:</p>
                  <p className="text-muted-foreground">English, Roman Urdu, Urdu</p>
                </div>
              </div>
            )}

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {messages.length === 0 && (
                <div className="text-center text-muted-foreground py-8 text-sm">
                  <p className="font-medium mb-1">Hi! I'm your AI assistant</p>
                  <p className="text-xs">Ask me to manage your tasks</p>
                </div>
              )}

              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${
                    message.role === "user" ? "justify-end" : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-3 py-2 text-sm ${
                      message.role === "user"
                        ? "bg-primary text-primary-foreground"
                        : "bg-muted text-foreground"
                    }`}
                  >
                    <p className="whitespace-pre-wrap">{message.content}</p>
                  </div>
                </div>
              ))}

              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-muted rounded-lg px-3 py-2">
                    <Loader2 className="h-4 w-4 animate-spin" />
                  </div>
                </div>
              )}

              {error && (
                <div className="text-xs text-destructive text-center py-2">
                  {error}
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="border-t border-border p-3">
              <div className="flex gap-2">
                <Textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Type a message..."
                  className="min-h-[40px] max-h-[80px] resize-none text-sm"
                  disabled={isLoading}
                  maxLength={2000}
                />
                <Button
                  onClick={handleSendMessage}
                  disabled={!input.trim() || isLoading}
                  size="icon"
                  className="h-[40px] w-[40px] flex-shrink-0"
                >
                  {isLoading ? (
                    <Loader2 className="h-4 w-4 animate-spin" />
                  ) : (
                    <Send className="h-4 w-4" />
                  )}
                </Button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
