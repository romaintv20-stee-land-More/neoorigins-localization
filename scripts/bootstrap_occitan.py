#!/usr/bin/env python3
"""Generate Occitan fallback localization by reusing the proven Norwegian bootstrap engine."""
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

source = source.replace("Norwegian Bokmål", "Occitan")
source = source.replace("Norwegian", "Occitan")
source = source.replace("norwegian_translation_cache.json", "occitan_translation_cache.json")
source = source.replace("build/no-discovery", "build/oc-discovery")
source = source.replace("no_no", "oc_fr")
source = source.replace("neoorigins_no_", "neoorigins_oc_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "oc", True]')
source = source.replace("max_chars: int = 3500", "max_chars: int = 1800")
source = source.replace(
    'SEPARATOR_RE = re.compile(r"\\n?ZXQSEP\\d{4}ZXQ\\n?")',
    'SEPARATOR_RE = re.compile(r"\\n?⟦\\s*\\d{4}\\s*⟧\\n?")',
)
source = source.replace(
    'f"\\nZXQSEP{index:04d}ZXQ\\n{value}"',
    'f"\\n⟦{index:04d}⟧\\n{value}"',
)
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "occitan_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_occitan.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_occitan.py"), "exec"), namespace)

# Use the public translation endpoint, with the mobile page as a conservative fallback.
def occitan_translate_rpc(text: str, attempts: int = 5):
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            params = urllib.parse.urlencode({
                "client": "gtx", "sl": "en", "tl": "oc", "dt": "t", "q": text,
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
                params = urllib.parse.urlencode({"sl": "en", "tl": "oc", "q": text})
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
    raise RuntimeError(f"Occitan translation failed after {attempts} attempts: {last_error}")

namespace["translate_rpc"] = occitan_translate_rpc

# Protect formatting/printf/tag tokens with punctuation-digit sentinels.
def occitan_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟪{index:04d}⟫"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def occitan_restore(text: str, tokens: list[str]):
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

namespace["protect"] = occitan_protect
namespace["restore"] = occitan_restore

# Preserve project branding and pre-seed short/high-visibility wording.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Dobrir lo creador d'Origin",
    "Mob Origin Creator": "Creador de Mob Origin",
    "Origin Architect": "Origin Architect",
    "Split": "Separar",
    "Elytra Boost": "Impulsion d'elitra",
    "Sonic Boom": "Explosion sonica",
    "Pack Bond": "Ligam de grop",
    "Speed Mining": "Minatge rapid",
    "Camoflauge": "Camoflatge",
    "Pack Boost": "Renfort del grop",
    "Max Mana Boost": "Aumentacion maximala de mana",
    "Rage Counter.": "Comptador de ràbia.",
    "Rage Counter": "Comptador de ràbia",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
