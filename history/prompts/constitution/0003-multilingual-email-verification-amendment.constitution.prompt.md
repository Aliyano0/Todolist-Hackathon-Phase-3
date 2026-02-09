---
id: 0003
title: Multilingual Email Verification Amendment
stage: constitution
date: 2026-02-09
surface: agent
model: claude-sonnet-4-5
feature: none
branch: main
user: Aliyan Aqeel
command: /sp.constitution
labels: ["constitution", "multilingual", "email-verification", "i18n", "roman-urdu", "urdu"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - None (constitution document)
---

## Prompt

Add one more thing in the constitution.md that it must have multilingual support with english as primary and roman urdu and urdu, detect the language base on the user input. email verification is required for the user to use the chatbot feature.

## Response snapshot

Updated constitution from v2.5.0 to v2.6.0 (MINOR version bump) to add multilingual support and email verification requirements.

**Key Changes:**

1. **Added Multilingual Support (Principle XI)**
   - Primary language: English
   - Supported languages: English, Roman Urdu, Urdu
   - Automatic language detection based on user input
   - AI agent responds in the detected language
   - Language detection per message (users can switch languages mid-conversation)
   - No translation of existing task data (tasks stored as-is in user's language)
   - Message model includes detected_language field

2. **Added Email Verification Requirements (Principle IX)**
   - Email verification required before accessing chatbot features
   - JWT token includes email_verified status (boolean)
   - Chat endpoint checks email_verified=true before allowing access
   - Returns 403 Forbidden with clear message if email not verified
   - Frontend displays email verification prompt for unverified users
   - Resend verification email functionality
   - Email verification link sent on registration
   - User model includes email_verified boolean field

3. **Updated Authentication Features:**
   - Added email verification to authentication flow
   - JWT token now contains email_verified claim
   - Email verification link sent on registration
   - Resend verification email functionality

4. **Updated Authorization & Data Isolation:**
   - Chat endpoint additionally requires email_verified=true
   - Unverified email attempting to access chat returns 403 Forbidden
   - Clear error message: "Email verification required to use chatbot"

5. **Updated Chat Endpoint:**
   - Requires valid JWT token with email_verified=true
   - Detects language from user input (English, Roman Urdu, Urdu)
   - Processes message through OpenAI Agents SDK with detected language context
   - Returns agent response in detected language

6. **Updated Frontend Chat Interface:**
   - Checks email_verified status before allowing chat access
   - Displays email verification prompt if email not verified
   - Provides "Resend Verification Email" button for unverified users
   - Supports multilingual UI based on detected language

7. **Updated Database Schema:**
   - User model: Added email_verified boolean field
   - Message model: Added detected_language field

8. **Updated Goals and Success Criteria:**
   - Primary goal includes multilingual support and email verification
   - Secondary goals include multilingual support and verified user access
   - Functional criteria include language detection and email verification

**Rationale:**
- Email verification reduces spam and ensures only legitimate users access the chatbot
- Multilingual support (English, Roman Urdu, Urdu) makes the chatbot accessible to a broader user base
- Automatic language detection provides seamless user experience without manual language selection

## Outcome

- ✅ Impact: Constitution successfully updated to v2.6.0 with multilingual support and email verification requirements. These additions enhance security (email verification) and accessibility (multilingual support) without breaking existing functionality.
- 🧪 Tests: None (constitution is a governance document, not code)
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: /sp.specify (update Phase 3 spec with multilingual and email verification), /sp.plan (design language detection and email verification flows), /sp.tasks (add i18n and email verification tasks)
- 🧠 Reflection: Email verification for chatbot access is a smart security measure that prevents spam and abuse while maintaining open access to basic todo features. Multilingual support with automatic language detection (English, Roman Urdu, Urdu) significantly expands the user base and provides a seamless experience. The per-message language detection allows users to switch languages naturally without manual configuration. Storing detected_language in the Message model enables future analytics and improvements to language detection accuracy.

## Evaluation notes (flywheel)

- Failure modes observed: None. Constitution update followed semantic versioning correctly (MINOR bump for new requirements). All sections updated consistently.
- Graders run and results (PASS/FAIL): PASS - Constitution validates against all requirements: version incremented correctly, dates updated, all affected sections modified consistently, rationale provided for new requirements.
- Prompt variant (if applicable): N/A (user request via conversation)
- Next experiment (smallest change to try): Implement language detection library evaluation (e.g., langdetect, fasttext) to determine best approach for detecting English, Roman Urdu, and Urdu. Consider edge cases like code-switching (mixing languages in one message).
