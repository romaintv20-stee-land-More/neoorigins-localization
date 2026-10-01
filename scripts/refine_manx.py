#!/usr/bin/env python3
"""Entry point for Manx refinement with source-normalization guards."""
import bootstrap_manx as base

# Empty localization values carry no semantic text to translate. Preserve them
# exactly and keep them away from external translation endpoints.
base.MANUAL_VALUES.setdefault("", "")

# Keep the established high-visibility UI term deterministic. Google sometimes
# renders the isolated button label "Search" as "Lhig", while the project QA
# baseline uses the direct Manx UI term "Ronsee".
base.MANUAL_VALUES["Search"] = "Ronsee"

import refine_manx_core

# Google's web translator can reinterpret marker-looking ASCII identifiers such
# as ZXQTK0001QXZ inside otherwise natural text. Use one Unicode Private Use
# character per protected token for the normal fast path. These are opaque in
# almost every translation while still letting us restore and verify each
# placeholder/technical token.
def protect_with_private_use(text: str) -> tuple[str, list[str]]:
    tokens: list[str] = []

    def repl(match):
        index = len(tokens)
        if index >= 0x1900:
            raise RuntimeError("Too many protected tokens in one localization value")
        marker = chr(0xE000 + index)
        tokens.append(match.group(0))
        return marker

    return refine_manx_core.GOOGLE_PROTECT_RE.sub(repl, text), tokens


def restore_private_use(text: str, tokens: list[str]) -> str:
    for index, token in enumerate(tokens):
        marker = chr(0xE000 + index)
        if marker not in text:
            raise refine_manx_core.BatchValidationError(
                f"Google translation lost protected token U+{ord(marker):04X}: {text!r}"
            )
        text = text.replace(marker, token)
    if any(0xE000 <= ord(char) <= 0xF8FF for char in text):
        raise refine_manx_core.BatchValidationError(
            f"Unexpected private-use token survived restoration: {text!r}"
        )
    return text


refine_manx_core.protect_for_google = protect_with_private_use
refine_manx_core.restore_google_tokens = restore_private_use

# Extremely token-dense strings can still make Google merge or duplicate adjacent
# Private Use characters. At singleton depth, avoid markers completely: translate
# only the natural-language spans between protected tokens, then splice the exact
# original tokens back into their original positions. This is intentionally a rare
# fallback; normal strings keep full-sentence context through the batched fast path.
def translate_preserving_structure(source: str) -> str:
    pieces: list[str] = []
    cursor = 0
    token_count = 0

    def translate_span(span: str) -> str:
        if not span or not span.strip():
            return span
        leading_len = len(span) - len(span.lstrip())
        trailing_len = len(span) - len(span.rstrip())
        leading = span[:leading_len]
        trailing = span[len(span) - trailing_len:] if trailing_len else ""
        body_end = len(span) - trailing_len if trailing_len else len(span)
        body = span[leading_len:body_end]
        if not body:
            return span
        return leading + refine_manx_core.google_request(body) + trailing

    for match in refine_manx_core.GOOGLE_PROTECT_RE.finditer(source):
        pieces.append(translate_span(source[cursor:match.start()]))
        pieces.append(match.group(0))
        token_count += 1
        cursor = match.end()
    pieces.append(translate_span(source[cursor:]))

    translated = "".join(pieces)
    if base.placeholder_signature(source) != base.placeholder_signature(translated):
        raise RuntimeError(
            f"Placeholder mismatch after structural Manx fallback: {source!r} -> {translated!r}"
        )
    print(
        f"Structural Manx fallback preserved {token_count} protected tokens for one dense value.",
        flush=True,
    )
    return translated


_original_google_translate_one = refine_manx_core.google_translate_one


def robust_google_translate_one(source: str) -> str:
    try:
        return _original_google_translate_one(source)
    except refine_manx_core.BatchValidationError as exc:
        print(f"Singleton token-marker fallback: {exc}", flush=True)
        return translate_preserving_structure(source)


refine_manx_core.google_translate_one = robust_google_translate_one

if __name__ == "__main__":
    refine_manx_core.main()
