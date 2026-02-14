"use client";

import { useState, useEffect, useRef } from "react";
import { sendChatMessage, ChatApiError } from "@/lib/chatApi";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Loader2, Send, Info } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: string;
}

interface ChatInterfaceProps {
  userId: string;
}

const STORAGE_KEY_PREFIX = "chat_shared_";

export function ChatInterface({ userId }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showInfo, setShowInfo] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load chat history from localStorage on mount
  useEffect(() => {
    if (userId) {
      const savedMessages = localStorage.getItem(`${STORAGE_KEY_PREFIX}messages_${userId}`);
      const savedConversationId = localStorage.getItem(`${STORAGE_KEY_PREFIX}conversation_${userId}`);

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
  }, [userId]);

  // Listen for chat updates from other components (e.g., ChatWidget)
  useEffect(() => {
    const handleChatUpdate = () => {
      if (userId) {
        const savedMessages = localStorage.getItem(`${STORAGE_KEY_PREFIX}messages_${userId}`);
        const savedConversationId = localStorage.getItem(`${STORAGE_KEY_PREFIX}conversation_${userId}`);

        if (savedMessages) {
          try {
            setMessages(JSON.parse(savedMessages));
          } catch (e) {
            console.error("Failed to reload chat history:", e);
          }
        }

        if (savedConversationId) {
          setConversationId(savedConversationId);
        }
      }
    };

    window.addEventListener("chatUpdated", handleChatUpdate);
    return () => window.removeEventListener("chatUpdated", handleChatUpdate);
  }, [userId]);

  // Save chat history to localStorage whenever messages change
  // Emit chatUpdated event AFTER saving to ensure other components get the latest data
  useEffect(() => {
    console.log("Messages state changed:", messages.length, "messages");
    console.log("Messages array:", messages);
    if (userId && messages.length > 0) {
      console.log("Saving to localStorage with key:", `${STORAGE_KEY_PREFIX}messages_${userId}`);
      localStorage.setItem(`${STORAGE_KEY_PREFIX}messages_${userId}`, JSON.stringify(messages));
      console.log("Saved to localStorage successfully");
      // Emit event AFTER saving to localStorage
      window.dispatchEvent(new CustomEvent("chatUpdated"));
      console.log("Emitted chatUpdated event");
    } else {
      console.log("Not saving - userId:", userId, "messages.length:", messages.length);
    }
  }, [messages, userId]);

  useEffect(() => {
    if (userId && conversationId) {
      localStorage.setItem(`${STORAGE_KEY_PREFIX}conversation_${userId}`, conversationId);
    }
  }, [conversationId, userId]);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

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
      const response = await sendChatMessage(userId, userMessage, conversationId);

      // Debug logging
      console.log("Chat API Response:", response);
      console.log("Response message:", response.message);
      console.log("Response type:", typeof response.message);

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
      console.log("Assistant message object:", assistantMessage);
      setMessages((prev) => [...prev, assistantMessage]);

      // Emit taskUpdated event for task list UI refresh
      // Note: chatUpdated event is emitted in useEffect after localStorage save
      window.dispatchEvent(new CustomEvent("taskUpdated"));
    } catch (err) {
      if (err instanceof ChatApiError) {
        setError(err.message);

        // Handle specific error codes
        if (err.errorCode === "EMAIL_NOT_VERIFIED") {
          // User should be redirected by parent component
          setError("Please verify your email to use the chatbot.");
        } else if (err.errorCode === "RATE_LIMIT_EXCEEDED") {
          setError("You're sending messages too quickly. Please wait a moment.");
        } else if (err.errorCode === "UNAUTHORIZED") {
          setError("Session expired. Please log in again.");
        }
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

  return (
    <div className="flex flex-col h-[600px] border border-border rounded-lg bg-card">
      {/* Header with Info Button */}
      <div className="flex items-center justify-between p-4 border-b border-border">
        <h2 className="text-lg font-semibold text-foreground">AI Assistant</h2>
        <button
          onClick={() => setShowInfo(!showInfo)}
          className="p-2 hover:bg-muted rounded-md transition-colors"
          aria-label="Show command guide"
        >
          <Info className="w-5 h-5 text-muted-foreground" />
        </button>
      </div>

      {/* Info Panel */}
      {showInfo && (
        <div className="bg-muted/30 border-b border-border p-4 text-sm space-y-3">
          <div>
            <p className="font-semibold text-foreground mb-2">Commands:</p>
            <ul className="space-y-1 text-muted-foreground">
              <li>• "Add task: [title]" - Create new task</li>
              <li>• "List my tasks" - Show all tasks with numbers</li>
              <li>• "Complete task #[number]" - Mark task as complete</li>
              <li>• "Delete task #[number]" - Remove task</li>
              <li>• "Update task #[number] title to [new title]" - Update task</li>
            </ul>
          </div>
          <div>
            <p className="font-semibold text-foreground mb-2">Supported Languages:</p>
            <p className="text-muted-foreground">English, Roman Urdu, Urdu</p>
          </div>
          <div>
            <p className="text-xs text-muted-foreground italic">
              Task numbers are shown in the dashboard. Use them to reference specific tasks.
            </p>
          </div>
        </div>
      )}

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-muted-foreground py-8">
            <p className="text-lg font-medium mb-2">Welcome to Todo AI Assistant</p>
            <p className="text-sm">
              Ask me to manage your tasks using natural language.
            </p>
            <p className="text-sm mt-2">
              Try: "Add task: buy groceries" or "List my tasks"
            </p>
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
              className={`max-w-[80%] rounded-lg px-4 py-2 ${
                message.role === "user"
                  ? "bg-primary text-primary-foreground"
                  : "bg-muted text-foreground"
              }`}
            >
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              <p className="text-xs opacity-70 mt-1">
                {new Date(message.timestamp).toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-muted rounded-lg px-4 py-2">
              <Loader2 className="h-4 w-4 animate-spin" />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Error Display */}
      {error && (
        <div className="px-4 pb-2">
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        </div>
      )}

      {/* Input Area */}
      <div className="border-t border-border p-4">
        <div className="flex gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me to manage your tasks..."
            className="min-h-[60px] max-h-[120px] resize-none"
            disabled={isLoading}
            maxLength={2000}
          />
          <Button
            onClick={handleSendMessage}
            disabled={!input.trim() || isLoading}
            size="icon"
            className="h-[60px] w-[60px]"
          >
            {isLoading ? (
              <Loader2 className="h-5 w-5 animate-spin" />
            ) : (
              <Send className="h-5 w-5" />
            )}
          </Button>
        </div>
        <p className="text-xs text-muted-foreground mt-2">
          Press Enter to send, Shift+Enter for new line
        </p>
      </div>
    </div>
  );
}
