#!/usr/bin/env python3
"""Generate Asturian fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Asturian")
source = source.replace("Norwegian", "Asturian")
source = source.replace("norwegian_translation_cache.json", "asturian_translation_cache.json")
source = source.replace("build/no-discovery", "build/ast-discovery")
source = source.replace("no_no", "ast_es")
source = source.replace("neoorigins_no_", "neoorigins_ast_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "ast", True]')
source = source.replace("max_chars: int = 3500", "max_chars: int = 1800")
# Use punctuation+digits separators so the translation service cannot lexicalize them.
source = source.replace(
    'SEPARATOR_RE = re.compile(r"\\n?ZXQSEP\\d{4}ZXQ\\n?")',
    'SEPARATOR_RE = re.compile(r"\\n?⟦\\s*\\d{4}\\s*⟧\\n?")',
)
source = source.replace(
    'f"\\nZXQSEP{index:04d}ZXQ\\n{value}"',
    'f"\\n⟦{index:04d}⟧\\n{value}"',
)
# Numbered printf placeholders may legitimately move with Asturian syntax.
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "asturian_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_asturian.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_asturian.py"), "exec"), namespace)

# The legacy Translate Webserver RPC returns a null payload for Asturian even though
# Asturian is available in the current Google Translate UI. Use the public web
# translation endpoint first, with the mobile page as a conservative fallback.
def asturian_translate_rpc(text: str, attempts: int = 5):
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            params = urllib.parse.urlencode({
                "client": "gtx", "sl": "en", "tl": "ast", "dt": "t", "q": text,
            })
            request = urllib.request.Request(
                "https://translate.googleapis.com/translate_a/single?" + params,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            raw = urllib.request.urlopen(request, timeout=60).read().decode("utf-8")
            payload = json.loads(raw)
            segments = payload[0] if isinstance(payload, list) and payload else None
            if isinstance(segments, list):
                translated = "".join(
                    segment[0]
                    for segment in segments
                    if isinstance(segment, list) and segment and isinstance(segment[0], str)
                )
                if translated:
                    return translated
            raise ValueError("Google single endpoint returned no translated segments")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, TypeError, IndexError, json.JSONDecodeError) as exc:
            last_error = exc
            try:
                params = urllib.parse.urlencode({"sl": "en", "tl": "ast", "q": text})
                request = urllib.request.Request(
                    "https://translate.google.com/m?" + params,
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                raw = urllib.request.urlopen(request, timeout=60).read().decode("utf-8")
                match = re.search(r'<div class="result-container">(.*?)</div>', raw, flags=re.S)
                if match:
                    translated = html.unescape(re.sub(r"<[^>]+>", "", match.group(1))).strip()
                    if translated:
                        return translated
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as fallback_exc:
                last_error = fallback_exc
            if attempt != attempts:
                time.sleep(2 ** (attempt - 1))
    raise RuntimeError(f"Asturian translation failed after {attempts} attempts: {last_error}")

namespace["translate_rpc"] = asturian_translate_rpc

# Protect formatting/printf/tag tokens with punctuation-digit sentinels. Tolerate
# whitespace and stripped delimiter glyphs, while the strict audit still checks all
# resulting placeholders after generation.
def asturian_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟪{index:04d}⟫"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def asturian_restore(text: str, tokens: list[str]):
    for index, token in enumerate(tokens):
        digits = f"{index:04d}"
        pattern = r"⟪\s*" + r"\s*".join(re.escape(ch) for ch in digits) + r"\s*⟫"
        text, count = re.subn(pattern, lambda _m, t=token: t, text)
        if count == 0:
            text = text.replace(f"⟪{digits}⟫", token)
        if token not in text:
            bare = rf"(?<!\d){re.escape(digits)}(?!\d)"
            text, _ = re.subn(bare, lambda _m, t=token: t, text, count=1)
    return text

namespace["protect"] = asturian_protect
namespace["restore"] = asturian_restore

# Preserve project branding and pre-seed short/high-visibility wording.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Abrir el creador d'Origin",
    "Mob Origin Creator": "Creador d'Origin de mobs",
    "Origin Architect": "Origin Architect",
    "Split": "Dixebrar",
    "Elytra Boost": "Impulsu d'élitros",
    "Sonic Boom": "Estruendu sónicu",
    "Pack Bond": "Vínculu de la manda",
    "Speed Mining": "Minería rápida",
    "Camoflauge": "Camuflaxe",
    "Pack Boost": "Impulsu de la manda",
    "Max Mana Boost": "Aumentu máximu de maná",
    "Rage Counter.": "Contador de furria.",
    "Rage Counter": "Contador de furria",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
