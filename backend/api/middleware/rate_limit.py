"""
Rate Limiting Middleware

Implements rate limiting for chat endpoints to prevent abuse.
Enforces 10 messages per minute per user.
"""

from fastapi import Request, HTTPException, status
from typing import Dict, List
from datetime import datetime, timedelta
import logging
from collections import defaultdict
import asyncio

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    In-memory rate limiter for chat endpoints

    Tracks message timestamps per user and enforces rate limits.
    Uses sliding window approach for accurate rate limiting.
    """

    def __init__(
        self,
        max_requests: int = 10,
        window_seconds: int = 60
    ):
        """
        Initialize rate limiter

        Args:
            max_requests: Maximum requests allowed per window (default: 10)
            window_seconds: Time window in seconds (default: 60)
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[datetime]] = defaultdict(list)
        self._cleanup_task = None

        logger.info(f"Initialized rate limiter: {max_requests} requests per {window_seconds}s")

    def _cleanup_old_entries(self):
        """Remove timestamps older than the window to prevent memory leaks"""
        cutoff_time = datetime.utcnow() - timedelta(seconds=self.window_seconds)

        for user_id in list(self.requests.keys()):
            # Filter out old timestamps
            self.requests[user_id] = [
                ts for ts in self.requests[user_id]
                if ts > cutoff_time
            ]

            # Remove user entry if no recent requests
            if not self.requests[user_id]:
                del self.requests[user_id]

    async def check_rate_limit(self, user_id: str) -> bool:
        """
        Check if user has exceeded rate limit

        Args:
            user_id: UUID of the user

        Returns:
            True if request is allowed, False if rate limit exceeded

        Raises:
            HTTPException 429: If rate limit is exceeded
        """
        now = datetime.utcnow()
        cutoff_time = now - timedelta(seconds=self.window_seconds)

        # Get user's recent requests
        user_requests = self.requests[user_id]

        # Remove old timestamps (sliding window)
        user_requests = [ts for ts in user_requests if ts > cutoff_time]
        self.requests[user_id] = user_requests

        # Check if limit exceeded
        if len(user_requests) >= self.max_requests:
            # Calculate time until oldest request expires
            oldest_request = min(user_requests)
            retry_after = int((oldest_request + timedelta(seconds=self.window_seconds) - now).total_seconds())

            logger.warning(f"Rate limit exceeded for user {user_id}: {len(user_requests)}/{self.max_requests} requests")

            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded: {self.max_requests} messages per {self.window_seconds} seconds",
                headers={"Retry-After": str(max(1, retry_after))}
            )

        # Add current request timestamp
        user_requests.append(now)
        self.requests[user_id] = user_requests

        logger.info(f"Rate limit check passed for user {user_id}: {len(user_requests)}/{self.max_requests} requests")
        return True

    async def start_cleanup_task(self):
        """Start background task to periodically clean up old entries"""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._periodic_cleanup())
            logger.info("Started rate limiter cleanup task")

    async def _periodic_cleanup(self):
        """Periodically clean up old entries every 5 minutes"""
        while True:
            try:
                await asyncio.sleep(300)  # 5 minutes
                self._cleanup_old_entries()
                logger.info(f"Rate limiter cleanup: {len(self.requests)} active users")
            except asyncio.CancelledError:
                logger.info("Rate limiter cleanup task cancelled")
                break
            except Exception as e:
                logger.error(f"Error in rate limiter cleanup: {str(e)}")

    def get_remaining_requests(self, user_id: str) -> int:
        """
        Get number of remaining requests for a user

        Args:
            user_id: UUID of the user

        Returns:
            Number of remaining requests in current window
        """
        now = datetime.utcnow()
        cutoff_time = now - timedelta(seconds=self.window_seconds)

        # Get user's recent requests
        user_requests = [ts for ts in self.requests[user_id] if ts > cutoff_time]

        return max(0, self.max_requests - len(user_requests))


# Global rate limiter instance
chat_rate_limiter = RateLimiter(max_requests=10, window_seconds=60)


async def rate_limit_dependency(user_id: str) -> bool:
    """
    FastAPI dependency for rate limiting

    Args:
        user_id: UUID of the user (from auth dependency)

    Returns:
        True if request is allowed

    Raises:
        HTTPException 429: If rate limit is exceeded
    """
    return await chat_rate_limiter.check_rate_limit(user_id)


__all__ = ['RateLimiter', 'chat_rate_limiter', 'rate_limit_dependency']
