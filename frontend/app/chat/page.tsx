"use client";

import { useAuth } from "@/providers/AuthProvider";
import { useRouter } from "next/navigation";
import { ChatInterface } from "@/components/chat/ChatInterface";
import { EmailVerificationPrompt } from "@/components/chat/EmailVerificationPrompt";
import { Loader2 } from "lucide-react";
import Navbar from "@/components/navigation/Navbar";
import ProtectedRoute from "@/components/auth/ProtectedRoute";

export default function ChatPage() {
  const { user, loading } = useAuth();
  const router = useRouter();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!user) {
    router.push("/login?redirect=/chat");
    return null;
  }

  // Show email verification prompt if not verified
  if (!user.email_verified) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-background">
          <Navbar />
          <EmailVerificationPrompt />
        </div>
      </ProtectedRoute>
    );
  }

  // Show chat interface for verified users
  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-background">
        <Navbar />
        <div className="container mx-auto px-4 py-8 max-w-4xl">
          <div className="mb-6">
            <h1 className="text-3xl font-bold text-foreground mb-2">AI Task Assistant</h1>
            <p className="text-muted-foreground">
              Manage your tasks using natural language. Try commands like "add task: buy groceries" or
              "list my tasks".
            </p>
          </div>

          <ChatInterface userId={user.id} />

          <div className="mt-6 p-4 bg-muted rounded-lg">
            <h2 className="text-sm font-semibold mb-2">Supported Commands:</h2>
            <ul className="text-sm text-muted-foreground space-y-1">
              <li>• Add task: "Add task: [task description]"</li>
              <li>• List tasks: "List my tasks" or "Show all tasks"</li>
              <li>• Complete task: "Complete task 1" or "Mark task 2 as done"</li>
              <li>• Delete task: "Delete task 3" or "Remove task 1"</li>
              <li>• Update task: "Update task 1 title to [new title]"</li>
            </ul>
            <p className="text-xs text-muted-foreground mt-2">
              Supports English, Roman Urdu, and Urdu languages.
            </p>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
