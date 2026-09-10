#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

project = ROOT / "PROJECT_HANDOFF.txt"
text = project.read_text(encoding="utf-8")

if "TAMIL / LANGUAGE #65 FINAL STATUS" in text:
    raise SystemExit("Tamil final status section already present")

replacements = [
    ("0.9.0 development currently has 64 locales:", "0.9.0 development currently has 65 locales:"),
    ("so_so, eo_uy, ky_kg.\n\nExpansion order so far:", "so_so, eo_uy, ky_kg, ta_in.\n\nExpansion order so far:"),
    ("- 64: Kyrgyz / ky_kg\n\nSIXTY-FOUR IS NOT THE FINAL TARGET.", "- 64: Kyrgyz / ky_kg\n- 65: Tamil / ta_in\n\nSIXTY-FIVE IS NOT THE FINAL TARGET."),
    ("- catalog.json says 64 supported locales", "- catalog.json says 65 supported locales"),
    ("- README.md says 64 languages and includes Kyrgyz ky_kg alongside the previously completed locales", "- README.md says 65 languages and includes Tamil ta_in alongside the previously completed locales"),
]
for old, new in replacements:
    if old not in text:
        raise SystemExit(f"Expected handoff marker not found: {old!r}")
    text = text.replace(old, new, 1)

section = r'''

TAMIL / LANGUAGE #65 FINAL STATUS
--------------------------------
Tamil locale: ta_in / தமிழ்.
Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, DOCUMENTED, AND READY/INTEGRATED THROUGH THE STANDARD FAST-FORWARD PROCESS.

Selection / staging:
- staging branch: release/0.9.0-tamil
- exact beta base used to create staging: 3cea648923ed56797976c08a437d6b8e0691bfba
- final three-target build source SHA: 1fe618c76fef2eb31c31229924100aca14e207d7
- NeoOrigins has zero official ta_in strings at all three pinned 2.2.27 refs
- all 10 supported 1.21.1 add-ons also had zero official ta_in strings at their audited refs

Architecture / packaging:
- 16 common namespaces: neoorigins_ta_common_01 through neoorigins_ta_common_16
- 1.21.1 delta namespace: neoorigins_ta_121
- 26.1.x overlay: ta_in inside neoorigins_26_1
- 26.2 overlay: ta_in inside neoorigins_26_2
- 1.21.1 packages 27 ta_in files = 16 common + 1 target delta + 10 add-ons
- 26.1.x packages 17 ta_in files = 16 common + correct modern overlay
- 26.2 packages 17 ta_in files = 16 common + correct modern overlay
- no wrong-version overlays or add-on files leak between targets
- packaged NeoOrigins keysets are exact and duplicate-free

Coverage / strict QA:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- all 10 supported 1.21.1 add-ons: complete
- missing: 0
- overlap: 0
- placeholder errors: 0
- scripts/validate.py: passed
- final contextual QA: 29 source files, 125,382 Tamil-script characters
- intentional Latin-only values are limited to JSON, NeoOrigins, Origin and Origin Architect
- final English/contextual-remnant guard passed
- official Minecraft Tamil terminology used in cleanup includes Night Vision = இரவு பார்வை and Rotten Flesh = அழுகிய சதை

Final three-target CI:
- workflow: .github/workflows/build-0.9.0-tamil.yml
- run: 34452266217
- source: 1fe618c76fef2eb31c31229924100aca14e207d7
- mc-1.21.1 job 102790466252: SUCCESS
  - artifact 10142050230
  - JAR SHA256 231686076894b26663d9f0373c4b3c47ebed6d72ebb63903e787ce92645fec69
  - artifact ZIP SHA256 57c73642ac86fb409c36134245ff939662d10b6187bad9710be8f34c17c62735
- mc-26.1.x job 102790465990: SUCCESS
  - artifact 10142041119
  - JAR SHA256 11c47ef075604fc5a4024e8c268a3503581d28d46da9185be0bce7d1cbaa4839
  - artifact ZIP SHA256 dda833380593609d5b7d5496c30716037de733f8a47347646f1a916fc05aa552
- mc-26.2 job 102790466194: SUCCESS
  - artifact 10142057119
  - JAR SHA256 a766230b80011bda25e92a5312d0997a995570e14becfb5a89d22331bc4babf1
  - artifact ZIP SHA256 b10e229c8b44913660b5507fb30af64b3193ffd0d30a61a8bb2437288e493104

NEXT LANGUAGE = #66.
Before starting #66, refetch release/0.9.0-beta and use its exact current HEAD as the staging base. Do not use main. Re-audit the current Minecraft Java locale inventory, apply the regional-variant dedup rule, verify official upstream strings before generating fallbacks, preserve placeholders exactly, run contextual QA, build all three targets, inspect JAR contents, and integrate only by non-forced fast-forward after confirming the staging branch is ahead-only.
'''
text = text.rstrip() + section + "\n"
project.write_text(text, encoding="utf-8")

next_handoff = ROOT / "NEXT_CHAT_HANDOFF.md"
next_handoff.write_text(r'''# NEXT CHAT HANDOFF — NeoOrigins Localization

## Source of truth

- Repository: `romaintv20-stee-land-More/neoorigins-localization`
- Current release branch: `release/0.9.0-beta`
- **Do not use `main`**: it is behind.
- Read `PROJECT_HANDOFF.txt` first.
- Completed language count: **65**.
- Last completed language: **#65 Tamil — `ta_in / தமிழ்`**.
- **Do not redo Tamil.**
- Next language: **#66**.
- The historical NeoOrigins 2.2.27 gaps in Italian, Polish, Russian, Simplified Chinese, Turkish, Czech and Hungarian were recovered before #59; do not treat that recovery as pending.

## #65 Tamil verification

Staging branch: `release/0.9.0-tamil`

Original beta base used for staging:
`3cea648923ed56797976c08a437d6b8e0691bfba`

Final three-target build source:
`1fe618c76fef2eb31c31229924100aca14e207d7`

NeoOrigins 2.2.27 refs:
- 1.21.1 `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2`
- 26.1.x `aa207ef14cf3b938e28b4081162701953957c1d5`
- 26.2 `511cadcafe3027d2a56b4448652ec9b74e2f3b07`

Coverage:
- 1.21.1: **2296/2296**
- 26.1.x: **2307/2307**
- 26.2: **2307/2307**

Strict QA:
- official Tamil strings upstream at audited refs: **0** for NeoOrigins and **0** for all 10 supported add-ons
- missing: **0**
- overlap: **0**
- placeholder errors: **0**
- all 10 supported 1.21.1 add-ons: strict success
- JSON validator: success
- contextual refinement: success
- final sanity: **29 files, 125,382 Tamil-script characters**
- intentional Latin-only values: `JSON`, `NeoOrigins`, `Origin`, `Origin Architect`
- final English/contextual-remnant guard: success
- official Minecraft Tamil terminology used in cleanup includes `இரவு பார்வை` for Night Vision and `அழுகிய சதை` for Rotten Flesh

## Final build run and artifacts

Run `34452266217`, source `1fe618c76fef2eb31c31229924100aca14e207d7`: all three jobs succeeded.

- 1.21.1 job `102790466252`, artifact `10142050230`, package **27/27**, JAR SHA256 `231686076894b26663d9f0373c4b3c47ebed6d72ebb63903e787ce92645fec69`, ZIP SHA256 `57c73642ac86fb409c36134245ff939662d10b6187bad9710be8f34c17c62735`
- 26.1.x job `102790465990`, artifact `10142041119`, package **17/17**, JAR SHA256 `11c47ef075604fc5a4024e8c268a3503581d28d46da9185be0bce7d1cbaa4839`, ZIP SHA256 `dda833380593609d5b7d5496c30716037de733f8a47347646f1a916fc05aa552`
- 26.2 job `102790466194`, artifact `10142057119`, package **17/17**, JAR SHA256 `a766230b80011bda25e92a5312d0997a995570e14becfb5a89d22331bc4babf1`, ZIP SHA256 `b10e229c8b44913660b5507fb30af64b3193ffd0d30a61a8bb2437288e493104`

Packaging semantics:
- 1.21.1: 16 common + `neoorigins_ta_121` + 10 add-ons = **27** Tamil files
- 26.1.x: 16 common + `neoorigins_26_1` = **17** Tamil files
- 26.2: 16 common + `neoorigins_26_2` = **17** Tamil files
- no wrong-version overlays or add-ons leak between targets
- packaged NeoOrigins keysets are exact and duplicate-free

## Start of language #66

1. Refetch `release/0.9.0-beta` and use its exact HEAD as the new staging base.
2. Re-read this file and `PROJECT_HANDOFF.txt`; do not use `main`.
3. Re-audit the current Minecraft Java locale inventory and apply the regional-variant dedup rule.
4. Verify NeoOrigins and all 10 add-ons for official translations before creating fallbacks.
5. Prefer official upstream strings, translate only missing keys, preserve placeholders exactly, and run contextual QA after machine generation.
6. Require strict NeoOrigins coverage **2296/2296, 2307/2307, 2307/2307**, plus all 10 add-ons, JSON validation and target-aware packaging.
7. Build all three targets and inspect JAR contents before integration.
8. Immediately before integration, refetch beta and staging; require staging to be ahead-only / `behind_by=0`, fast-forward with `force=false`, then verify both refs are identical.
''', encoding="utf-8")

print("Tamil handoffs finalized: 65 locales, #65 complete, next #66")
