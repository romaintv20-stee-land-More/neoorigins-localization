#!/usr/bin/env python3
"""Entry point for Hawaiian refinement with robust placeholder protection."""
import bootstrap_hawaiian as base

# Empty localization values carry no semantic text to translate.
base.MANUAL_VALUES.setdefault("", "")

import refine_hawaiian_core

# Use one Unicode Private Use character per protected token. Google generally
# preserves these opaque markers more reliably than ASCII marker-looking strings.
def protect_with_private_use(text: str) -> tuple[str, list[str]]:
    tokens: list[str] = []

    def repl(match):
        index = len(tokens)
        if index >= 0x1900:
            raise RuntimeError("Too many protected tokens in one localization value")
        marker = chr(0xE000 + index)
        tokens.append(match.group(0))
        return marker

    return refine_hawaiian_core.GOOGLE_PROTECT_RE.sub(repl, text), tokens


def restore_private_use(text: str, tokens: list[str]) -> str:
    for index, token in enumerate(tokens):
        marker = chr(0xE000 + index)
        if marker not in text:
            raise refine_hawaiian_core.BatchValidationError(
                f"Google translation lost protected token U+{ord(marker):04X}: {text!r}"
            )
        text = text.replace(marker, token)
    if any(0xE000 <= ord(char) <= 0xF8FF for char in text):
        raise refine_hawaiian_core.BatchValidationError(
            f"Unexpected private-use token survived restoration: {text!r}"
        )
    return text


refine_hawaiian_core.protect_for_google = protect_with_private_use
refine_hawaiian_core.restore_google_tokens = restore_private_use

# Token-dense strings can still cause adjacent opaque markers to be merged or
# duplicated. At singleton depth, translate only natural-language spans and splice
# the original protected tokens back into their exact structural positions.
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
        return leading + refine_hawaiian_core.google_request(body) + trailing

    for match in refine_hawaiian_core.GOOGLE_PROTECT_RE.finditer(source):
        pieces.append(translate_span(source[cursor:match.start()]))
        pieces.append(match.group(0))
        token_count += 1
        cursor = match.end()
    pieces.append(translate_span(source[cursor:]))

    translated = "".join(pieces)
    if base.placeholder_signature(source) != base.placeholder_signature(translated):
        raise RuntimeError(
            f"Placeholder mismatch after structural Hawaiian fallback: {source!r} -> {translated!r}"
        )
    print(
        f"Structural Hawaiian fallback preserved {token_count} protected tokens for one dense value.",
        flush=True,
    )
    return translated


_original_google_translate_one = refine_hawaiian_core.google_translate_one


def robust_google_translate_one(source: str) -> str:
    try:
        return _original_google_translate_one(source)
    except refine_hawaiian_core.BatchValidationError as exc:
        print(f"Singleton token-marker fallback: {exc}", flush=True)
        return translate_preserving_structure(source)


refine_hawaiian_core.google_translate_one = robust_google_translate_one

if __name__ == "__main__":
    refine_hawaiian_core.main()
