"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { ChatInterface } from "@/components/chat/ChatInterface";
import { EmailVerificationPrompt } from "@/components/chat/EmailVerificationPrompt";
import { Loader2 } from "lucide-react";

interface User {
  id: string;
  email: string;
  emailVerified: boolean;
  name?: string;
}

export default function ChatPage() {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check authentication status
    const checkAuth = async () => {
      try {
        // Get user session from Better Auth
        const response = await fetch("/api/auth/session", {
          credentials: "include",
        });

        if (!response.ok) {
          // Not authenticated, redirect to login
          router.push("/login?redirect=/chat");
          return;
        }

        const session = await response.json();

        if (!session.user) {
          router.push("/login?redirect=/chat");
          return;
        }

        setUser({
          id: session.user.id,
          email: session.user.email,
          emailVerified: session.user.emailVerified || false,
          name: session.user.name,
        });
      } catch (error) {
        console.error("Auth check failed:", error);
        router.push("/login?redirect=/chat");
      } finally {
        setIsLoading(false);
      }
    };

    checkAuth();
  }, [router]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!user) {
    return null; // Will redirect
  }

  // Show email verification prompt if not verified
  if (!user.emailVerified) {
    return <EmailVerificationPrompt />;
  }

  // Show chat interface for verified users
  return (
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
  );
}
