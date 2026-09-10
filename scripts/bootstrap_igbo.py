#!/usr/bin/env python3
"""Generate Igbo fallback localization by reusing the proven Norwegian bootstrap engine."""
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
def igbo_translate_rpc(text: str, attempts: int = 7):
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
            # The mobile fallback is useful for transient endpoint failures, but
            # not as a high-rate alternate. It is tried once per primary failure.
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
                # Longer bounded backoff is intentional after the observed 429.
                time.sleep(min(30, 2 ** attempt))
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

# Probe separators before using them. Igbo translation rewrote the earlier
# human-readable delimiter. Private-use/control-style sentinels are tested on a
# tiny sample and only a separator that round-trips with the correct item count
# is accepted. This preserves the low-request batch workflow without trusting an
# unverified delimiter.
SEPARATOR_CANDIDATES = [
    (lambda i: f"\ue000{i:04d}\ue001", re.compile(r"\ue000\s*\d{4}\s*\ue001")),
    (lambda i: f"␞{i:04d}␟", re.compile(r"␞\s*\d{4}\s*␟")),
    (lambda i: f"ZZQXSEP{i:04d}QXZZ", re.compile(r"ZZQXSEP\s*\d{4}\s*QXZZ", re.I)),
]


def choose_separator():
    sample = ["Stone", "Night vision", "Choose a class", "Player speed"]
    for maker, splitter in SEPARATOR_CANDIDATES:
        joined = sample[0] + "".join(f"\n{maker(i)}\n{value}" for i, value in enumerate(sample[1:], 1))
        translated = igbo_translate_rpc(joined)
        parts = splitter.split(translated)
        print(f"Igbo separator probe {maker(1)!r}: {len(parts)}/{len(sample)} parts")
        if len(parts) == len(sample):
            return maker, splitter
    raise RuntimeError("No tested Igbo batch separator survived translation")


def igbo_translate_values(values: list[str]):
    cache_path = namespace["CACHE_PATH"]
    cache = namespace["read_json"](cache_path) if cache_path.exists() else {}
    pending = list(dict.fromkeys(value for value in values if value not in cache))
    batches = namespace["make_batches"](pending, max_chars=1500, max_items=24)
    print(f"Igbo cache: {len(cache)} entries; {len(pending)} new strings in {len(batches)} verified-separator batches")
    if not pending:
        return cache

    maker, splitter = choose_separator()
    for batch_number, batch in enumerate(batches, 1):
        protected = []
        token_sets = []
        for value in batch:
            masked, tokens = igbo_protect(value)
            protected.append(masked)
            token_sets.append(tokens)
        joined = protected[0] + "".join(
            f"\n{maker(index)}\n{value}" for index, value in enumerate(protected[1:], 1)
        )
        translated_joined = igbo_translate_rpc(joined)
        translated = splitter.split(translated_joined)
        if len(translated) != len(batch):
            raise RuntimeError(
                f"Igbo batch {batch_number}: verified separator later failed; expected {len(batch)} strings, received {len(translated)}"
            )
        for source_text, result, tokens in zip(batch, translated, token_sets):
            result = igbo_restore(result, tokens).strip()
            expected = sorted(namespace["PLACEHOLDER_RE"].findall(source_text))
            actual = sorted(namespace["PLACEHOLDER_RE"].findall(result))
            if expected != actual:
                raise RuntimeError(f"Placeholder mismatch after translation: {source_text!r} -> {result!r}")
            cache[source_text] = result
        namespace["write_json"](cache_path, cache)
        print(f"Translated Igbo batch {batch_number}/{len(batches)} ({len(cache)} cached strings)")
        time.sleep(0.25)
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
