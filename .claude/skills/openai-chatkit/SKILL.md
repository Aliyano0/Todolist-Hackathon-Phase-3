---
name: openai-chatkit
description: Integrate conversational AI chat interfaces into web apps. Use when setting up chat UIs for user input, message display, and state management, especially in /chat routes with JWT auth and multilingual support.
---

# OpenAI ChatKit Skill

## Description
A frontend toolkit for integrating conversational AI chat interfaces into web applications. Use this skill for setting up chat UIs that handle user input, display messages, and manage conversation state.

## Instructions
- Install via npm: `npm install @openai/chatkit`.
- Integrate into the /chat route: Import ChatKit components like `<ChatProvider>`, `<ChatInput>`, and `<MessageList>`.
- Persist conversation_id using React state or localStorage to maintain session across reloads.
- Handle JWT authentication: Include Authorization header in API calls to /api/{user_id}/chat.
- For email verification: Conditionally render a prompt if API returns 403 "email_not_verified", with a button to call Better Auth's resend verification endpoint.
- Support Dark mode: Use CSS variables or theme providers to match the app's styling.
- Multilingual: Detect language from user input and adjust UI placeholders accordingly.

## Examples
Example code snippet:
```jsx
import { ChatProvider, ChatInput, MessageList } from '@openai/chatkit';
import { useState } from 'react';

function ChatPage() {
  const [conversationId, setConversationId] = useState(localStorage.getItem('convId') || null);
  // ... (handle API calls, verification check)
  return (
    <ChatProvider>
      <MessageList conversationId={conversationId} />
      <ChatInput onSend={(message) => handleSend(message, conversationId)} />
    </ChatProvider>
  );
}
```


### Best Practices
 Ensure smooth animations for message loading, handle tool_calls in responses by displaying them as structured outputs (e.g., task lists).