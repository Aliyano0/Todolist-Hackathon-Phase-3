"""
OpenRouter API Client

Wrapper for OpenRouter API to handle LLM inference with retry logic and error handling.
Uses gpt-4o-mini model for cost-efficient chat completions.
"""

from typing import List, Dict, Any, Optional
import aiohttp
import asyncio
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class OpenRouterError(Exception):
    """Base exception for OpenRouter API errors"""
    pass


class OpenRouterRateLimitError(OpenRouterError):
    """Raised when rate limit is exceeded"""
    pass


class OpenRouterAuthError(OpenRouterError):
    """Raised when authentication fails"""
    pass


class OpenRouterClient:
    """
    Client for OpenRouter API with retry logic and error handling

    OpenRouter provides access to multiple LLM models through a unified API.
    This client uses gpt-4o-mini for cost-efficient inference.
    """

    BASE_URL = "https://openrouter.ai/api/v1"
    DEFAULT_MODEL = "openai/gpt-4o-mini"
    MAX_RETRIES = 3
    INITIAL_RETRY_DELAY = 1.0  # seconds
    MAX_RETRY_DELAY = 10.0  # seconds

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize OpenRouter client

        Args:
            api_key: OpenRouter API key (defaults to OPENROUTER_API_KEY env var)
            model: Model to use (defaults to gpt-4o-mini)
            timeout: Request timeout in seconds (default: 30)
        """
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            raise ValueError("OpenRouter API key is required (OPENROUTER_API_KEY)")

        self.model = model or self.DEFAULT_MODEL
        self.timeout = timeout

        logger.info(f"Initialized OpenRouter client with model: {self.model}")

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        tools: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Create a chat completion with retry logic

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0.0 to 2.0)
            max_tokens: Maximum tokens to generate (optional)
            tools: List of tool definitions for function calling (optional)

        Returns:
            API response dictionary with completion

        Raises:
            OpenRouterError: If API request fails after retries
            OpenRouterRateLimitError: If rate limit is exceeded
            OpenRouterAuthError: If authentication fails
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens

        if tools:
            payload["tools"] = tools

        # Retry with exponential backoff
        retry_delay = self.INITIAL_RETRY_DELAY
        last_error = None

        for attempt in range(self.MAX_RETRIES):
            try:
                return await self._make_request(payload)

            except OpenRouterRateLimitError as e:
                last_error = e
                if attempt < self.MAX_RETRIES - 1:
                    logger.warning(f"Rate limit hit, retrying in {retry_delay}s (attempt {attempt + 1}/{self.MAX_RETRIES})")
                    await asyncio.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, self.MAX_RETRY_DELAY)
                else:
                    logger.error(f"Rate limit exceeded after {self.MAX_RETRIES} retries")
                    raise

            except OpenRouterAuthError as e:
                # Don't retry auth errors
                logger.error(f"Authentication failed: {str(e)}")
                raise

            except OpenRouterError as e:
                last_error = e
                if attempt < self.MAX_RETRIES - 1:
                    logger.warning(f"API error, retrying in {retry_delay}s (attempt {attempt + 1}/{self.MAX_RETRIES}): {str(e)}")
                    await asyncio.sleep(retry_delay)
                    retry_delay = min(retry_delay * 2, self.MAX_RETRY_DELAY)
                else:
                    logger.error(f"API request failed after {self.MAX_RETRIES} retries: {str(e)}")
                    raise

        # Should not reach here, but just in case
        raise last_error or OpenRouterError("Request failed after retries")

    async def _make_request(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make HTTP request to OpenRouter API

        Args:
            payload: Request payload

        Returns:
            API response dictionary

        Raises:
            OpenRouterError: If request fails
            OpenRouterRateLimitError: If rate limit is exceeded
            OpenRouterAuthError: If authentication fails
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/todolist-hackathon",  # Optional but recommended
            "X-Title": "Todo AI Chatbot"  # Optional but recommended
        }

        url = f"{self.BASE_URL}/chat/completions"

        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload, headers=headers) as response:
                    response_data = await response.json()

                    # Handle different status codes
                    if response.status == 200:
                        logger.info(f"Chat completion successful (model: {self.model})")
                        return response_data

                    elif response.status == 401:
                        error_msg = response_data.get("error", {}).get("message", "Authentication failed")
                        raise OpenRouterAuthError(f"Authentication error: {error_msg}")

                    elif response.status == 429:
                        error_msg = response_data.get("error", {}).get("message", "Rate limit exceeded")
                        raise OpenRouterRateLimitError(f"Rate limit error: {error_msg}")

                    else:
                        error_msg = response_data.get("error", {}).get("message", f"HTTP {response.status}")
                        raise OpenRouterError(f"API error: {error_msg}")

        except aiohttp.ClientError as e:
            logger.error(f"HTTP client error: {str(e)}")
            raise OpenRouterError(f"Network error: {str(e)}")

        except asyncio.TimeoutError:
            logger.error(f"Request timeout after {self.timeout}s")
            raise OpenRouterError(f"Request timeout after {self.timeout}s")

        except Exception as e:
            logger.error(f"Unexpected error in OpenRouter request: {str(e)}")
            raise OpenRouterError(f"Unexpected error: {str(e)}")

    def extract_message_content(self, response: Dict[str, Any]) -> str:
        """
        Extract message content from API response

        Args:
            response: API response dictionary

        Returns:
            Message content string

        Raises:
            OpenRouterError: If response format is invalid
        """
        try:
            return response["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            logger.error(f"Invalid response format: {str(e)}")
            raise OpenRouterError(f"Invalid response format: {str(e)}")

    def extract_tool_calls(self, response: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """
        Extract tool calls from API response (for function calling)

        Args:
            response: API response dictionary

        Returns:
            List of tool call dictionaries or None if no tool calls

        Raises:
            OpenRouterError: If response format is invalid
        """
        try:
            message = response["choices"][0]["message"]
            return message.get("tool_calls")
        except (KeyError, IndexError) as e:
            logger.error(f"Invalid response format: {str(e)}")
            raise OpenRouterError(f"Invalid response format: {str(e)}")


__all__ = [
    'OpenRouterClient',
    'OpenRouterError',
    'OpenRouterRateLimitError',
    'OpenRouterAuthError'
]
