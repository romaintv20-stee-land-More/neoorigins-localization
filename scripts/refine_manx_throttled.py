#!/usr/bin/env python3
"""Run the full Manx refinement with aggressively throttled Google batching.

This driver reuses `refine_manx.py`'s translation and QA logic, but replaces its
network scheduler. The previous 340-batch/10-worker run hit Google's anonymous rate
limit. Here we use POST requests, larger batches, one worker, exponential 429 backoff,
and recursive validated splits only when a batch separator is genuinely damaged.
"""
from __future__ import annotations

from concurrent.futures import Future
from urllib.parse import urlencode
import json
import random
import re
import time
import urllib.error
import urllib.request

import refine_manx as r


class SequentialExecutor:
    """Tiny Executor-compatible wrapper that executes submitted calls immediately."""

    def __init__(self, max_workers=None):
        self.max_workers = max_workers

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def submit(self, fn, *args, **kwargs):
        future = Future()
        try:
            future.set_result(fn(*args, **kwargs))
        except BaseException as exc:  # propagate through Future.result(), like Executor
            future.set_exception(exc)
        return future


def make_large_batches(sources: list[str], max_items: int = 64, max_chars: int = 3200) -> list[list[str]]:
    batches: list[list[str]] = []
    current: list[str] = []
    chars = 0
    for source in sources:
        projected = chars + len(source) + (24 if current else 0)
        if current and (len(current) >= max_items or projected > max_chars):
            batches.append(current)
            current = []
            chars = 0
        current.append(source)
        chars += len(source) + 24
    if current:
        batches.append(current)
    return batches


def throttled_google_request(masked: str) -> str:
    body = urlencode(
        {
            "client": "gtx",
            "sl": "en",
            "tl": "gv",
            "dt": "t",
            "ie": "UTF-8",
            "oe": "UTF-8",
            "q": masked,
        }
    ).encode("utf-8")

    last_error: Exception | None = None
    for attempt in range(9):
        try:
            request = urllib.request.Request(
                r.GOOGLE_ENDPOINT,
                data=body,
                method="POST",
                headers={
                    "User-Agent": "Mozilla/5.0 NeoOrigins-Manx-Localization/1.0",
                    "Accept": "application/json,text/plain,*/*",
                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                },
            )
            with urllib.request.urlopen(request, timeout=45) as response:
                payload = json.loads(response.read().decode("utf-8"))
            segments = payload[0]
            translated = "".join(segment[0] for segment in segments if segment and segment[0])
            if not translated.strip():
                raise RuntimeError("Google returned an empty translation")
            # Keep request cadence deliberately low even on success.
            time.sleep(0.55 + random.random() * 0.20)
            return translated
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code == 429:
                retry_after = exc.headers.get("Retry-After") if exc.headers else None
                try:
                    server_wait = float(retry_after) if retry_after else 0.0
                except ValueError:
                    server_wait = 0.0
                wait = max(server_wait, min(15.0 * (2 ** attempt), 180.0)) + random.random() * 2.0
                print(f"Google 429 on batch request; cooling down {wait:.1f}s (attempt {attempt + 1}/9)")
                time.sleep(wait)
                continue
            if attempt == 8:
                break
            time.sleep(min(2.0 * (2 ** attempt), 30.0) + random.random())
        except (urllib.error.URLError, TimeoutError, RuntimeError, ValueError) as exc:
            last_error = exc
            if attempt == 8:
                break
            time.sleep(min(2.0 * (2 ** attempt), 30.0) + random.random())
    raise RuntimeError(f"Google Manx throttled request failed: {last_error}")


def validated_batch(sources: list[str]) -> dict[str, str]:
    if len(sources) == 1:
        return {sources[0]: r.google_translate_one(sources[0])}

    protected = [r.protect_for_google(source) for source in sources]
    pieces: list[str] = []
    for index, (masked, _) in enumerate(protected):
        pieces.append(masked)
        if index + 1 < len(protected):
            pieces.append(f"\nZXQSEP{index:04d}QXZ\n")
    joined = "".join(pieces)

    try:
        translated_joined = throttled_google_request(joined)
        matches = list(r.BATCH_SEPARATOR_RE.finditer(translated_joined))
        if len(matches) != len(sources) - 1:
            raise RuntimeError(
                f"separator count mismatch: expected {len(sources) - 1}, found {len(matches)}"
            )

        parts: list[str] = []
        start = 0
        for expected, match in enumerate(matches):
            if int(match.group(1)) != expected:
                raise RuntimeError(
                    f"separator order mismatch: expected {expected}, got {match.group(1)}"
                )
            parts.append(translated_joined[start:match.start()].strip())
            start = match.end()
        parts.append(translated_joined[start:].strip())

        result: dict[str, str] = {}
        for source, translated, (_, tokens) in zip(sources, parts, protected):
            translated = r.restore_google_tokens(translated, tokens)
            if r.base.placeholder_signature(source) != r.base.placeholder_signature(translated):
                raise RuntimeError(f"placeholder mismatch: {source!r} -> {translated!r}")
            if not translated.strip():
                raise RuntimeError(f"empty translation for {source!r}")
            result[source] = translated
        return result
    except RuntimeError as exc:
        # Validation damage is handled by splitting, never by exploding into dozens of
        # simultaneous one-string requests. Network 429s are already retried above.
        if len(sources) <= 2:
            raise
        middle = len(sources) // 2
        print(f"Splitting invalid Manx batch of {len(sources)} strings: {exc}")
        left = validated_batch(sources[:middle])
        right = validated_batch(sources[middle:])
        left.update(right)
        return left


def main() -> None:
    r.ThreadPoolExecutor = SequentialExecutor
    r.make_batches = make_large_batches
    r.google_request = throttled_google_request
    r.google_translate_batch = validated_batch
    r.main()


if __name__ == "__main__":
    main()
