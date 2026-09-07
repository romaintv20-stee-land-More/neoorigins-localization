#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "scripts/audit_origins_fantasy_upstream.py",
    "scripts/audit_origins_backgrounds_upstream.py",
    "scripts/audit_origins_more_backgrounds_upstream.py",
    "scripts/audit_origins_backgrounds_iss_upstream.py",
    "scripts/audit_origins_furries_upstream.py",
    "scripts/audit_origins_classes_extended_upstream.py",
    "scripts/audit_origins_classes_iss_upstream.py",
    "scripts/audit_origin_architect_upstream.py",
]
for rel in FILES:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if '"ja_jp"' in text:
        print(rel, "already enabled")
        continue
    old = '"cs_cz", "hu_hu")'
    if old not in text:
        raise SystemExit(f"Expected locale tail not found in {rel}")
    path.write_text(text.replace(old, '"cs_cz", "hu_hu", "ja_jp")', 1), encoding="utf-8")
    print(rel, "enabled")
