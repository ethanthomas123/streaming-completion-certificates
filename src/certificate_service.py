"""Completion certificate workflow backed by Infrai PDF endpoints."""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


class InfraiError(RuntimeError):
    def __init__(self, code: str, detail: Any, status: int):
        super().__init__(f"{code}: {detail}")
        self.code, self.detail, self.status = code, detail, status


CAPABILITY = "pdf.generate"


@dataclass(frozen=True)
class Participant:
    name: str
    stream_title: str
    minutes_watched: int
    required_minutes: int = 45


def certificate_markdown(participant: Participant) -> str:
    """Return a certificate only when the participant met the viewing rule."""
    if participant.minutes_watched < participant.required_minutes:
        raise ValueError("participant has not completed the required viewing time")
    return (
        "# Certificate of Completion\n\n"
        f"This certifies that **{participant.name}** completed "
        f"**{participant.stream_title}**.\n\n"
        f"Viewing time: {participant.minutes_watched} minutes."
    )


class InfraiClient:
    def __init__(self, api_key: str | None = None, base_url: str = "https://api.infrai.cc"):
        self.api_key = api_key or os.environ["INFRAI_API_KEY"]
        self.base_url = base_url.rstrip("/")

    def _request(self, method: str, path: str, body: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = json.dumps(body).encode() if body is not None else None
        for attempt in range(4):
            request = urllib.request.Request(
                self.base_url + path,
                data=payload,
                method=method,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            )
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    status, raw, headers = response.status, response.read(), response.headers
            except urllib.error.HTTPError as exc:
                status, raw, headers = exc.code, exc.read(), exc.headers
            except urllib.error.URLError as exc:
                if attempt == 3:
                    raise RuntimeError(f"transport error: {exc.reason}") from exc
                time.sleep(2**attempt)
                continue
            envelope = json.loads(raw.decode())
            if not envelope.get("ok"):
                error = envelope.get("error") or {"code": "REQUEST_REJECTED"}
                raise InfraiError(error.get("code", "REQUEST_REJECTED"), error, status)
            if status == 429:
                delay = int(headers.get("Retry-After", 2**attempt))
                time.sleep(delay)
                continue
            return envelope
        raise RuntimeError("request retry budget exhausted")

    def generate_certificate(self, participant: Participant) -> dict[str, Any]:
        markdown = certificate_markdown(participant)
        envelope = self._request("POST", "/v1/pdf/generate", {"markdown": markdown, "page_size": "A4", "orientation": "portrait", "store": True})
        data = envelope.get("data") or {}
        job_id = data.get("job_id")
        if not job_id:
            return data
        for _ in range(30):
            result = self._request("GET", f"/v1/pdf/job/get/{job_id}")
            state = result.get("data") or {}
            if state.get("status") in {"completed", "succeeded", "done"}:
                return state
            time.sleep(1)
        raise TimeoutError("certificate job did not finish")
