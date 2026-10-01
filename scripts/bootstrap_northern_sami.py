#!/usr/bin/env python3
"""Generate Northern Sami fallback localization using the hardened Igbo bootstrap engine."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "scripts/bootstrap_igbo.py").read_text(encoding="utf-8")

# Reuse the hardened separator probing, batching and token isolation while
# changing only the locale/language identity and Google target language.
source = source.replace("Igbo", "Northern Sami")
source = source.replace("igbo", "northern_sami")
source = source.replace("ig_ng", "se_no")
source = source.replace("neoorigins_ig_", "neoorigins_se_")
source = source.replace("build/ig-discovery", "build/se-discovery")
source = source.replace('[[text, "en", "ig", True]', '[[text, "en", "se", True]')
source = source.replace('"tl": "ig"', '"tl": "se"')
source = source.replace("'tl': 'ig'", "'tl': 'se'")

# Do not inherit Igbo seed wording. Let the supported Northern Sami translation
# target translate those values normally, while preserving project branding.
source, count = re.subn(
    r'namespace\["MANUAL_OVERRIDES"\] = \{.*?\}\n\nnamespace\["write_json"\]',
    'namespace["MANUAL_OVERRIDES"] = {\n    "Origin Architect": "Origin Architect",\n}\n\nnamespace["write_json"]',
    source,
    count=1,
    flags=re.S,
)
if count != 1:
    raise RuntimeError("Could not replace inherited Igbo manual overrides")

namespace = {
    "__name__": "northern_sami_bootstrap",
    "__file__": str(ROOT / "scripts/bootstrap_northern_sami.py"),
}
exec(compile(source, str(ROOT / "scripts/bootstrap_northern_sami.py"), "exec"), namespace)
