#!/usr/bin/env python3
"""Run the full strict Traditional Chinese (Taiwan) localization bootstrap."""
from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "src/main/resources/resourcepacks/fallback_localizations/assets"
LOCALE = "zh_tw"

ADDON_AUDITS = [
    ("scripts/audit_medievalorigins_upstream.py", ["--ref", "1.21.1-fabric"]),
    ("scripts/audit_ibarnorigins_upstream.py", ["--ref", "multiloader-1.21.1-new-pack-format"]),
    ("scripts/audit_origins_fantasy_upstream.py", []),
    ("scripts/audit_origins_backgrounds_upstream.py", []),
    ("scripts/audit_origins_more_backgrounds_upstream.py", []),
    ("scripts/audit_origins_backgrounds_iss_upstream.py", []),
    ("scripts/audit_origins_furries_upstream.py", []),
    ("scripts/audit_origins_classes_extended_upstream.py", []),
    ("scripts/audit_origins_classes_iss_upstream.py", []),
    ("scripts/audit_origin_architect_upstream.py", []),
]

NEO_REFS = [
    ("af467a3bc118f6bbc0970d68f7e03fa631d7e6f2", "mc-1.21.1", ["--fallback-namespace-glob", "neoorigins_zhtw_common_*", "--extra-namespace", "neoorigins_zhtw_121"]),
    ("aa207ef14cf3b938e28b4081162701953957c1d5", "mc-26.1", ["--fallback-namespace-glob", "neoorigins_zhtw_common_*", "--extra-namespace", "neoorigins_26_1"]),
    ("511cadcafe3027d2a56b4448652ec9b74e2f3b07", "mc-26.2", ["--fallback-namespace-glob", "neoorigins_zhtw_common_*", "--extra-namespace", "neoorigins_26_2"]),
]


def run(*args: str) -> None:
    print("+", " ".join(args), flush=True)
    subprocess.run(args, cwd=ROOT, check=True)


def restrict_addon_audits() -> None:
    for filename, _ in ADDON_AUDITS:
        path = ROOT / filename
        text = path.read_text(encoding="utf-8")
        updated, count = re.subn(r"^LOCALES\s*=.*$", 'LOCALES = ("zh_tw",)', text, count=1, flags=re.M)
        if count == 0:
            updated, count = re.subn(r"^DEFAULT_LOCALES\s*=.*$", 'DEFAULT_LOCALES = ("zh_tw",)', text, count=1, flags=re.M)
        if count != 1:
            raise RuntimeError(f"Could not patch locale list in {filename}")
        path.write_text(updated, encoding="utf-8")


def discover() -> None:
    for ref, label, _ in NEO_REFS:
        run(
            "python3", "scripts/audit_neoorigins_upstream.py",
            "--ref", ref,
            "--output", f"build/zhtw-discovery-{label}",
            "--locale", LOCALE,
        )
    for filename, extra in ADDON_AUDITS:
        run("python3", filename, *extra)


def generate_and_prune() -> None:
    run("python3", "scripts/bootstrap_traditional_chinese.py")
    for filename, extra in ADDON_AUDITS:
        run("python3", filename, *extra, "--prune")


def strict_audit() -> None:
    for ref, label, fallback_args in NEO_REFS:
        run(
            "python3", "scripts/audit_neoorigins_upstream.py",
            "--ref", ref,
            "--output", f"build/zhtw-audit-{label}",
            "--locale", LOCALE,
            *fallback_args,
            "--fail-on-overlap", "--fail-on-missing", "--fail-on-placeholders",
        )
    for filename, extra in ADDON_AUDITS:
        run(
            "python3", filename, *extra,
            "--fail-on-overlap", "--fail-on-missing", "--fail-on-placeholders",
        )
    run("python3", "scripts/validate.py")


def sanity_check() -> None:
    files = list(ASSETS.glob("**/lang/zh_tw.json"))
    if len(files) != 29:
        raise RuntimeError(f"Expected 29 zh_tw localization files, found {len(files)}")
    values = [str(v) for path in files for v in json.loads(path.read_text(encoding="utf-8")).values()]
    text = "\n".join(values)
    han_chars = len(re.findall(r"[\u3400-\u4DBF\u4E00-\u9FFF]", text))
    traditional_signals = len(re.findall(r"[體與為這們來時會無後裡擊傷讓還種開關戰網選擇學習實獲發應過處圖書經對傳變顯氣龍門間風點敵護裝態範]", text))
    lexical_markers = len(re.findall(r"(?:玩家|傷害|生命|攻擊|能力|可以|使用|獲得|速度|時間|如果|無法|效果|力量|目標|敵人|冷卻|持續|增加|減少|造成)", text))
    if han_chars < 30000:
        raise RuntimeError(f"Traditional Chinese Han-character sanity too low: {han_chars}")
    if traditional_signals < 1000:
        raise RuntimeError(f"Traditional Chinese orthographic sanity too low: {traditional_signals}")
    if lexical_markers < 500:
        raise RuntimeError(f"Traditional Chinese lexical sanity too low: {lexical_markers}")
    print(
        f"Traditional Chinese text sanity passed: {han_chars} Han chars, "
        f"{traditional_signals} traditional signals, {lexical_markers} lexical markers "
        f"across {len(files)} files"
    )


def add_packaging_switch() -> None:
    path = ROOT / "build.gradle"
    text = path.read_text(encoding="utf-8")
    if "includeTraditionalChinese121Translations" in text:
        return

    anchor = "def includeTatar121Translations = (project.findProperty('include_tatar_121_translations') ?: defaultInclude121Translations.toString()).toBoolean()\n"
    if anchor not in text:
        raise RuntimeError("Tatar Gradle definition anchor not found")
    text = text.replace(
        anchor,
        anchor + "def includeTraditionalChinese121Translations = (project.findProperty('include_traditional_chinese_121_translations') ?: defaultInclude121Translations.toString()).toBoolean()\n",
        1,
    )

    anchor = "    inputs.property 'include_tatar_121_translations', includeTatar121Translations\n"
    if anchor not in text:
        raise RuntimeError("Tatar Gradle input anchor not found")
    text = text.replace(
        anchor,
        anchor + "    inputs.property 'include_traditional_chinese_121_translations', includeTraditionalChinese121Translations\n",
        1,
    )

    anchor = "    if (!includeTatar121Translations) {\n        exclude 'resourcepacks/fallback_localizations/assets/neoorigins_tt_121/**'\n    }\n"
    if anchor not in text:
        raise RuntimeError("Tatar Gradle exclusion anchor not found")
    text = text.replace(
        anchor,
        anchor + "\n    if (!includeTraditionalChinese121Translations) {\n        exclude 'resourcepacks/fallback_localizations/assets/neoorigins_zhtw_121/**'\n    }\n",
        1,
    )
    path.write_text(text, encoding="utf-8")


def main() -> None:
    restrict_addon_audits()
    discover()
    generate_and_prune()
    strict_audit()
    sanity_check()
    add_packaging_switch()


if __name__ == "__main__":
    main()
