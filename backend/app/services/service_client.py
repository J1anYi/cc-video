import httpx
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = "closed"  # closed, open, half-open

    async def call(self, func, *args, **kwargs):
        if self.state == "open":
            if self._should_attempt_recovery():
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is open")

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise e

    def _should_attempt_recovery(self) -> bool:
        if not self.last_failure_time:
            return True
        elapsed = (datetime.utcnow() - self.last_failure_time).total_seconds()
        return elapsed >= self.recovery_timeout

    def _on_success(self):
        self.failure_count = 0
        self.state = "closed"

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        if self.failure_count >= self.failure_threshold:
            self.state = "open"


class ServiceClient:
    def __init__(
        self,
        base_url: str,
        service_name: str,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        self.base_url = base_url.rstrip("/")
        self.service_name = service_name
        self.timeout = timeout
        self.max_retries = max_retries
        self.circuit_breaker = CircuitBreaker()
        self.client = httpx.AsyncClient(timeout=timeout)

    async def request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        request_headers = headers or {}
        request_headers["X-Service-Name"] = self.service_name

        async def make_request():
            for attempt in range(self.max_retries):
                try:
                    response = await self.client.request(
                        method=method,
                        url=url,
                        headers=request_headers,
                        json=json_data,
                        params=params,
                    )
                    response.raise_for_status()
                    return response.json()
                except httpx.HTTPStatusError as e:
                    if e.response.status_code >= 500 and attempt < self.max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    raise
                except httpx.RequestError as e:
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    raise

        return await self.circuit_breaker.call(make_request)

    async def get(self, path: str, **kwargs) -> Dict[str, Any]:
        return await self.request("GET", path, **kwargs)

    async def post(self, path: str, **kwargs) -> Dict[str, Any]:
        return await self.request("POST", path, **kwargs)

    async def put(self, path: str, **kwargs) -> Dict[str, Any]:
        return await self.request("PUT", path, **kwargs)

    async def delete(self, path: str, **kwargs) -> Dict[str, Any]:
        return await self.request("DELETE", path, **kwargs)

    async def health_check(self) -> bool:
        try:
            response = await self.client.get(f"{self.base_url}/health")
            return response.status_code == 200
        except Exception:
            return False

    async def close(self):
        await self.client.aclose()


class ServiceClientFactory:
    _clients: Dict[str, ServiceClient] = {}

    @classmethod
    def get_client(cls, service_name: str, base_url: str) -> ServiceClient:
        if service_name not in cls._clients:
            cls._clients[service_name] = ServiceClient(base_url, service_name)
        return cls._clients[service_name]

    @classmethod
    async def close_all(cls):
        for client in cls._clients.values():
            await client.close()
        cls._clients.clear()
