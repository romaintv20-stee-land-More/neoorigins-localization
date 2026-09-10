#!/usr/bin/env python3
"""Generate Igbo fallback localization by reusing the proven Norwegian bootstrap engine."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_norwegian.py").read_text(encoding="utf-8")

source = source.replace("Norwegian Bokmål", "Igbo")
source = source.replace("Norwegian", "Igbo")
source = source.replace("norwegian_translation_cache.json", "igbo_translation_cache.json")
source = source.replace("build/no-discovery", "build/ig-discovery")
source = source.replace("no_no", "ig_ng")
source = source.replace("neoorigins_no_", "neoorigins_ig_")
source = source.replace('[[text, "en", "no", True]', '[[text, "en", "ig", True]')
source = source.replace(
    "if PLACEHOLDER_RE.findall(source) != PLACEHOLDER_RE.findall(result):",
    "if sorted(PLACEHOLDER_RE.findall(source)) != sorted(PLACEHOLDER_RE.findall(result)):",
)

namespace = {"__name__": "igbo_bootstrap", "__file__": str(ROOT / "scripts/bootstrap_igbo.py")}
exec(compile(source, str(ROOT / "scripts/bootstrap_igbo.py"), "exec"), namespace)

# Public translation endpoint with the mobile page as a conservative fallback.
def igbo_translate_rpc(text: str, attempts: int = 5):
    last_error = None
    for attempt in range(1, attempts + 1):
        try:
            params = urllib.parse.urlencode({
                "client": "gtx", "sl": "en", "tl": "ig", "dt": "t", "q": text,
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
                params = urllib.parse.urlencode({"sl": "en", "tl": "ig", "q": text})
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
    raise RuntimeError(f"Igbo translation failed after {attempts} attempts: {last_error}")

namespace["translate_rpc"] = igbo_translate_rpc

# Protect formatting/printf/tag tokens with punctuation-digit sentinels.
def igbo_protect(text: str):
    tokens = []
    def replace(match):
        index = len(tokens)
        tokens.append(match.group(0))
        return f"⟪{index:04d}⟫"
    return namespace["TOKEN_RE"].sub(replace, text), tokens


def igbo_restore(text: str, tokens: list[str]):
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

namespace["protect"] = igbo_protect
namespace["restore"] = igbo_restore

# Igbo translation can rewrite or remove synthetic separators in multi-string
# requests. Translate each source string independently, in bounded parallelism,
# so item boundaries and placeholders never depend on separator survival.
def igbo_translate_values(values: list[str]):
    cache_path = namespace["CACHE_PATH"]
    cache = namespace["read_json"](cache_path) if cache_path.exists() else {}
    pending = list(dict.fromkeys(value for value in values if value not in cache))
    print(f"Igbo cache: {len(cache)} entries; {len(pending)} new strings translated independently")

    def translate_one(source_text: str):
        masked, tokens = igbo_protect(source_text)
        result = igbo_translate_rpc(masked)
        result = igbo_restore(result, tokens).strip()
        expected = sorted(namespace["PLACEHOLDER_RE"].findall(source_text))
        actual = sorted(namespace["PLACEHOLDER_RE"].findall(result))
        if expected != actual:
            raise RuntimeError(f"Placeholder mismatch after translation: {source_text!r} -> {result!r}")
        return source_text, result

    if pending:
        completed = 0
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = {executor.submit(translate_one, value): value for value in pending}
            for future in as_completed(futures):
                source_text, result = future.result()
                cache[source_text] = result
                completed += 1
                if completed % 50 == 0 or completed == len(pending):
                    namespace["write_json"](cache_path, cache)
                    print(f"Translated {completed}/{len(pending)} pending Igbo strings ({len(cache)} cached)")
        namespace["write_json"](cache_path, cache)
    return cache

namespace["translate_values"] = igbo_translate_values

# Preserve project branding and pre-seed short/high-visibility wording.
namespace["MANUAL_OVERRIDES"] = {
    "Open Origin Creator": "Mepee onye okike Origin",
    "Mob Origin Creator": "Onye okike Mob Origin",
    "Origin Architect": "Origin Architect",
    "Split": "Kewaa",
    "Elytra Boost": "Nkwalite Elytra",
    "Sonic Boom": "Mgbawa ụda",
    "Pack Bond": "Njikọ otu",
    "Speed Mining": "Ngwuputa ngwa ngwa",
    "Camoflauge": "Mkpuchi",
    "Pack Boost": "Nkwalite otu",
    "Max Mana Boost": "Nkwalite mana kachasị",
    "Rage Counter.": "Onụọgụ iwe.",
    "Rage Counter": "Onụọgụ iwe",
}

namespace["write_json"](namespace["CACHE_PATH"], namespace["MANUAL_OVERRIDES"])
namespace["main"]()
