"""Circuit breaker pattern for graceful degradation."""
import time
from enum import Enum
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)


class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject all requests
    HALF_OPEN = "half_open"  # Testing if service recovered


class CircuitBreaker:
    """
    Circuit breaker for external service calls.
    Prevents cascading failures by failing fast when a service is down.
    """

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
        expected_exception: type = Exception,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = CircuitState.CLOSED

    def _should_allow_request(self) -> bool:
        """Check if request should be allowed through."""
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            # Check if recovery timeout has passed
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                logger.info(f"Circuit breaker {self.name} entering HALF_OPEN state")
                return True
            return False

        # HALF_OPEN: allow one request to test
        return True

    def _record_success(self):
        """Record successful request."""
        self.failure_count = 0
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            logger.info(f"Circuit breaker {self.name} recovered, entering CLOSED state")

    def _record_failure(self):
        """Record failed request."""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            logger.warning(f"Circuit breaker {self.name} failed in HALF_OPEN, back to OPEN")
        elif self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(
                f"Circuit breaker {self.name} entering OPEN state after {self.failure_count} failures"
            )

    async def call(self, func: Callable, fallback: Callable = None, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection.

        Args:
            func: Async function to execute
            fallback: Optional fallback function if circuit is open
            *args, **kwargs: Arguments to pass to func

        Returns:
            Result of func or fallback

        Raises:
            Exception: If circuit is open and no fallback provided
        """
        if not self._should_allow_request():
            if fallback:
                logger.info(f"Circuit breaker {self.name} OPEN, using fallback")
                return await fallback(*args, **kwargs)
            raise Exception(f"Circuit breaker {self.name} is OPEN")

        try:
            result = await func(*args, **kwargs)
            self._record_success()
            return result
        except self.expected_exception as e:
            self._record_failure()
            if fallback:
                logger.info(f"Circuit breaker {self.name} caught exception, using fallback: {e}")
                return await fallback(*args, **kwargs)
            raise


# Global circuit breakers for external services
# Can be extended for Redis, external APIs, etc.
circuit_breakers: dict[str, CircuitBreaker] = {}


def get_circuit_breaker(name: str, **kwargs) -> CircuitBreaker:
    """Get or create a circuit breaker by name."""
    if name not in circuit_breakers:
        circuit_breakers[name] = CircuitBreaker(name, **kwargs)
    return circuit_breakers[name]
