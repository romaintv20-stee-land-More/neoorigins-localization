#!/usr/bin/env python3
"""Entry point for Manx refinement with source-normalization guards."""
import bootstrap_manx as base

# Empty localization values carry no semantic text to translate. Preserve them
# exactly and keep them away from external translation endpoints.
base.MANUAL_VALUES.setdefault("", "")

import refine_manx_core

# Google's web translator can reinterpret marker-looking ASCII identifiers such
# as ZXQTK0001QXZ inside otherwise natural text. Use one Unicode Private Use
# character per protected token instead. These are opaque to translation while
# still letting us restore and verify every original placeholder/technical token.
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

if __name__ == "__main__":
    refine_manx_core.main()
