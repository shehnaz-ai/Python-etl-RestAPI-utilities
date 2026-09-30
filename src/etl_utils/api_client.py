from __future__ import annotations
from . import logger
import requests
import logging


from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class APIClient:
    """Reusable REST API client with retry support."""

    def __init__(self,
                 base_url: str | None = None,
                 timeout: int = 30,
                 max_retries: int = 3,
                 backoff_factor: float = 0.5,
                 headers: dict[str, str] | None = None,
                 ):
            self.base_url = base_url.rstrip("/") if base_url else ""
            self.timeout = timeout
            self.session = requests.Session()
            retry_strategy = Retry(
                total=max_retries,
                connect=max_retries,
                read=max_retries,
                status=max_retries,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET", "POST", "PUT", "DELETE"],
                raise_on_status=False,
                respect_retry_after_header=True
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            self.session.mount("https://", adapter)
            self.session.mount("http://", adapter)
            if headers:
                self.session.headers.update(headers)

    def _build_url(self, endpoint: str) -> str:
        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint

        if not self.base_url:
            return endpoint

        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def get(self, endpoint: str, params:dict | None = None,headers: dict[str, str] | None = None) -> Any:
        """Send GET request and return JSON response."""
        url = self._build_url(endpoint)
        try:
            logger.info("Sending GET request: %s", url)
            response = self.session.get(url, params=params,headers=headers, timeout=self.timeout)
            response.raise_for_status()
            logger.info("API request successful: status=%s",response.status_code)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.exception("API request failed: %s", url)
            raise

    def close(self) -> None:
        """Close the HTTP session."""
        self.session.close()

    def __enter__(self):
            return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback
    ):
        self.close()

"""Why use Session?

A requests.Session allows you to reuse HTTP connections and configure shared behavior such as 
retry policies.

Why use retries?

Some failures are temporary:

HTTP 429: Too many requests
HTTP 500: Internal server error
HTTP 502: Bad gateway
HTTP 503: Service unavailable
HTTP 504: Gateway timeout

Retrying can help recover from transient failures.

Note: Retry configuration should be adapted to the API's requirements. We restrict automatic retries 
to GET requests here because retrying write operations can cause duplicate side effects if implemented 
carelessly."""