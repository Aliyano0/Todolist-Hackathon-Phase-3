"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Mail, Loader2, CheckCircle2, AlertCircle } from "lucide-react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export function EmailVerificationPrompt() {
  const [isResending, setIsResending] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);

  const handleResendEmail = async () => {
    setIsResending(true);
    setMessage(null);

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_BASE_URL}/api/auth/resend-verification`, {
        method: "POST",
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        setMessage({
          type: "success",
          text: "Verification email sent! Please check your inbox and spam folder.",
        });
      } else {
        const error = await response.json().catch(() => ({ detail: "Failed to send email" }));
        setMessage({
          type: "error",
          text: error.detail || "Failed to send verification email. Please try again.",
        });
      }
    } catch (error) {
      setMessage({
        type: "error",
        text: "Network error. Please check your connection and try again.",
      });
    } finally {
      setIsResending(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-200px)] p-4">
      <Card className="max-w-md w-full">
        <CardHeader className="text-center">
          <div className="flex justify-center mb-4">
            <div className="rounded-full bg-primary/10 p-3">
              <Mail className="h-8 w-8 text-primary" />
            </div>
          </div>
          <CardTitle className="text-2xl">Email Verification Required</CardTitle>
          <CardDescription>
            Please verify your email address to access the AI chatbot feature.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Alert>
            <AlertCircle className="h-4 w-4" />
            <AlertTitle>Check Your Inbox</AlertTitle>
            <AlertDescription>
              We've sent a verification link to your email address. Click the link to verify your
              account and unlock the chatbot feature.
            </AlertDescription>
          </Alert>

          {message && (
            <Alert variant={message.type === "error" ? "destructive" : "default"}>
              {message.type === "success" ? (
                <CheckCircle2 className="h-4 w-4" />
              ) : (
                <AlertCircle className="h-4 w-4" />
              )}
              <AlertDescription>{message.text}</AlertDescription>
            </Alert>
          )}

          <div className="space-y-2">
            <Button
              onClick={handleResendEmail}
              disabled={isResending}
              className="w-full"
              variant="outline"
            >
              {isResending ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Sending...
                </>
              ) : (
                <>
                  <Mail className="mr-2 h-4 w-4" />
                  Resend Verification Email
                </>
              )}
            </Button>

            <p className="text-xs text-center text-muted-foreground">
              Didn't receive the email? Check your spam folder or click the button above to resend.
            </p>
          </div>

          <div className="pt-4 border-t border-border">
            <p className="text-sm text-muted-foreground text-center">
              After verifying your email, refresh this page to access the chatbot.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
