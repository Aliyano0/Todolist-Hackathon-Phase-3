/**
 * Chat API Client
 *
 * Handles communication with the backend chat endpoint.
 * Automatically attaches JWT token via httpOnly cookies.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  conversation_id: string;
  message: string;
  timestamp: string;
}

export class ChatApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public errorCode?: string
  ) {
    super(message);
    this.name = "ChatApiError";
  }
}

/**
 * Send a chat message to the AI agent
 *
 * @param userId - User ID from authenticated session
 * @param message - User's message (1-2000 characters)
 * @param conversationId - Optional conversation ID to continue existing conversation
 * @returns Chat response with agent's message
 * @throws ChatApiError for various error conditions
 */
export async function sendChatMessage(
  userId: string,
  message: string,
  conversationId?: string
): Promise<ChatResponse> {
  try {
    // Get JWT token from localStorage
    const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };

    // Add Authorization header if token exists
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
      method: "POST",
      credentials: "include",
      headers,
      body: JSON.stringify({
        message,
        conversation_id: conversationId,
      }),
    });

    // Handle specific error cases
    if (response.status === 401) {
      throw new ChatApiError(
        "Authentication required. Please log in again.",
        401,
        "UNAUTHORIZED"
      );
    }

    if (response.status === 403) {
      const error = await response.json().catch(() => ({ detail: "Access denied" }));
      throw new ChatApiError(
        error.detail || "Please verify your email to use the chatbot",
        403,
        "EMAIL_NOT_VERIFIED"
      );
    }

    if (response.status === 429) {
      throw new ChatApiError(
        "You're sending messages too quickly. Please wait a moment.",
        429,
        "RATE_LIMIT_EXCEEDED"
      );
    }

    if (response.status === 500) {
      throw new ChatApiError(
        "AI service temporarily unavailable. Please try again later.",
        500,
        "SERVER_ERROR"
      );
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Request failed" }));
      throw new ChatApiError(
        error.detail || "Failed to send message",
        response.status
      );
    }

    return await response.json();
  } catch (error) {
    if (error instanceof ChatApiError) {
      throw error;
    }

    // Network or other errors
    throw new ChatApiError(
      "Network error. Please check your connection and try again.",
      0,
      "NETWORK_ERROR"
    );
  }
}
