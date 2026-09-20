"""Online Jev provider with strict response validation and injectable transport."""

from __future__ import annotations

import json
import os
from collections.abc import Callable, Mapping
from typing import Any
from urllib import error, request

from .contracts import SystemOneRequest, SystemOneResponse


Transport = Callable[[str, Mapping[str, str], bytes, float], Mapping[str, Any]]


class TypeSafeHTTPProvider:
    """Minimal documented HTTP adapter; secrets are never stored in artifacts.

    The official Python SDK remains the recommended production client.  This
    dependency-free adapter exists so the repository can run identical
    contracts against Jev and local open implementations.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        endpoint: str = "https://api.typesafe.ai/v1/systemone",
        timeout_seconds: float = 30.0,
        transport: Transport | None = None,
    ) -> None:
        self.api_key = api_key or os.environ.get("TYPESAFE_API_KEY", "")
        if not self.api_key:
            raise ValueError("TYPESAFE_API_KEY is required for the online Jev backend")
        if not endpoint.startswith("https://"):
            raise ValueError("the TypeSafe endpoint must use https")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self.endpoint = endpoint
        self.timeout_seconds = timeout_seconds
        self.transport = transport or _urlopen_transport

    def decide(self, decision: SystemOneRequest) -> SystemOneResponse:
        body = json.dumps(decision.to_dict(), ensure_ascii=False).encode("utf-8")
        payload = self.transport(
            self.endpoint,
            {
                "authorization": f"Bearer {self.api_key}",
                "content-type": "application/json",
                "accept": "application/json",
            },
            body,
            self.timeout_seconds,
        )
        response = SystemOneResponse.from_payload(payload)
        missing = set(decision.questions) - set(response.answers)
        extra = set(response.answers) - set(decision.questions)
        if missing or extra:
            raise ValueError(
                f"response question mismatch; missing={sorted(missing)}, extra={sorted(extra)}"
            )
        return response


def _urlopen_transport(
    endpoint: str,
    headers: Mapping[str, str],
    body: bytes,
    timeout_seconds: float,
) -> Mapping[str, Any]:
    outgoing = request.Request(endpoint, data=body, headers=dict(headers), method="POST")
    try:
        with request.urlopen(outgoing, timeout=timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        raise RuntimeError(f"TypeSafe API returned HTTP {exc.code}") from exc
    except error.URLError as exc:
        raise RuntimeError("TypeSafe API request failed") from exc
    if not isinstance(payload, Mapping):
        raise ValueError("TypeSafe API response must be an object")
    return payload
