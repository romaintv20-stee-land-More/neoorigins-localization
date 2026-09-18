#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

repls = {
    '0.9.0 development currently has 57 locales:': '0.9.0 development currently has 58 locales:',
    'af_za, az_az, kn_in.\n\nExpansion order so far:': 'af_za, az_az, kn_in, cv_cu.\n\nExpansion order so far:',
    '- 57: Kannada / kn_in\n\nFIFTY-SEVEN IS NOT THE FINAL TARGET.': '- 57: Kannada / kn_in\n- 58: Chuvash / cv_cu\n\nFIFTY-EIGHT IS NOT THE FINAL TARGET.',
    '50. NEXT ACTION\n---------------\nNEXT LANGUAGE = language 58.': '51. NEXT ACTION\n---------------\nNEXT LANGUAGE = language 59.',
}
for old, new in repls.items():
    if old not in text:
        raise SystemExit(f'PROJECT_HANDOFF expected text missing: {old!r}')
    text = text.replace(old, new, 1)

section = '''50. CHUVASH 0.9.0 STATUS
-------------------------
Chuvash locale: cv_cu / Чӑвашла.
Minecraft language metadata verified from the current Java 26.2 assets:
- language.code: chv_RU-CU
- language.name: Чӑвашла
- language.region: Чӑваш Ен, Раҫҫей

Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, AND DOCUMENTED.

Selection rationale:
- Chuvash is a current Minecraft Java locale introduced in the 26.2 language set.
- It is a distinct language, not a regional duplicate of any of the first 57 locales.
- Swiss French was deliberately not selected because the project deduplicates near-identical regional variants.

Staging:
- branch: release/0.9.0-chuvash
- exact beta base used to create staging: aab61dca5f901f26be0cd1c59886c812c1709d07
- pre-handoff documented staging head: d0ed7687962d0052583e9822b3782d884160471f
- final build source SHA: 74308d879cfe67b8821653ae622fe2917d2e2051

NeoOrigins pinned refs:
- 1.21.1: 860ecdb24e723983e93004ea8ceb5de90ccf0d70
- 26.1.x: 3c1c7365507679c836d3c14af5d4dd0654652e87
- 26.2: 65864716a5a796fa1c51ec3e8a6d9640abebb4ca

Architecture:
- 16 common namespaces: neoorigins_cv_common_01 through neoorigins_cv_common_16
- 1.21.1 delta namespace: neoorigins_cv_121
- 26.1.x overlay: cv_cu inside neoorigins_26_1
- 26.2 overlay: cv_cu inside neoorigins_26_2
- all 10 supported/licensed add-ons receive cv_cu fallback files on 1.21.1

Coverage / strict audits:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- missing: 0
- overlap: 0
- placeholder errors: 0
- all 10 add-on audits: complete with 0 missing / 0 overlap / 0 placeholder errors
- scripts/validate.py: passed
- final Chuvash script sanity: 16,744 Chuvash-specific letters across 29 cv_cu files

Contextual terminology QA:
- initial report workflow: run 34380576719, job 102564138958
- initial report exposed real false friends rather than being treated as sufficient proof by itself
- corrected examples include Origin (proper project term), Power -> ability/capability semantics, On/Off UI semantics, official Minecraft Night Vision = Ҫӗрлехи куҫ, Nether = Незер, Netherite = Незерит, anatomical Scales, Pavlov, Apply, Spawn Rules, Drops/Loot, XP/Experience, Origin Architect, Ultimine, mana, Elytra and hotkeys
- deterministic refinement workflow: run 34398767552, job 102625101585, success
- strict audits and contextual guard assertions passed after refinement

Bootstrap / generation evidence:
- bootstrap run: 34379807657
- bootstrap job: 102561580556
- bootstrap/audit artifact ID: 10115475171
- artifact SHA256: c3699e4ad25b4ef6cef8128cf2a3bd033b9d05a6390961edb83faebe55303c93

Metadata evidence:
- metadata run: 34398994850
- metadata job: 102625846393
- catalog.json supported_locale_count = 58
- catalog.json, CATALOG.md and README.md include cv_cu / Чӑвашла / Tchouvache and the 3-version coverage

Final build evidence:
- build run: 34398870533
- source SHA: 74308d879cfe67b8821653ae622fe2917d2e2051
- 1.21.1 job 102625439066: success; packaging 27 / 27 cv_cu files
  - artifact ID 10122670078
  - JAR SHA256 feb1b1a528ad3735cf3146f9a797f5e2fe3a6cd7bf818892a9ce5958062ff91b
  - artifact ZIP SHA256 7481f9e487a82ebac091497e76d7f943496c20e66770c27f7b8a188b3a41049b
- 26.1.x job 102625438886: success; packaging 17 / 17 cv_cu files
  - artifact ID 10122652529
  - JAR SHA256 a95b6a5938ea8c0ea221059f8cf94c467bd18e430b962576035006e6005186b4
  - artifact ZIP SHA256 c39180ca5c221f9906f71c33ff830de7be69acc7397486c1ab25ea118f99da42
- 26.2 job 102625438481: success; packaging 17 / 17 cv_cu files
  - artifact ID 10122650555
  - JAR SHA256 6886fd8ab2371c953bcad00135aed29dc586cbd48d86880afd064f840cd1b549
  - artifact ZIP SHA256 563d21fcb6c299bef1d6daf677f8609252c2ed8c8782cfc343c057b721de77d5

Packaging semantics verified by CI:
- 1.21.1 = 16 common + neoorigins_cv_121 + 10 add-ons = 27; no 26.x Chuvash overlays
- 26.1.x = 16 common + neoorigins_26_1 = 17; no add-ons and no neoorigins_cv_121
- 26.2 = 16 common + neoorigins_26_2 = 17; no add-ons and no neoorigins_cv_121

Integration discipline:
- release/0.9.0-beta must be refetched immediately before integration.
- Only fast-forward release/0.9.0-beta to the exact release/0.9.0-chuvash HEAD when compare shows staging is ahead-only and behind_by=0.
- Never force-push.
- After integration, release/0.9.0-beta and release/0.9.0-chuvash must resolve to the exact same SHA; refetch branch refs rather than trusting a stale literal SHA in this handoff.

NEXT LANGUAGE after Chuvash = language 59.
Re-evaluate the current Minecraft Java locale inventory at that time, prefer a useful distinct language not already in the 58-locale set, verify official upstream strings first, and apply the regional-variant dedup rule before generating fallbacks.

'''
marker = '51. NEXT ACTION\n---------------\nNEXT LANGUAGE = language 59.'
if section in text:
    raise SystemExit('Chuvash section already present')
if marker not in text:
    raise SystemExit('Renumbered NEXT ACTION marker missing')
text = text.replace(marker, section + marker, 1)
p.write_text(text, encoding='utf-8')

next_chat = '''# NEXT CHAT HANDOFF — NeoOrigins Localization\n\n## Source of truth\n\n- Repository: `romaintv20-stee-land-More/neoorigins-localization`\n- Current release branch: `release/0.9.0-beta`\n- **Do not use `main`**: it is behind.\n- Read `PROJECT_HANDOFF.txt` first.\n- Completed language count: **58**.\n- Last completed language: **#58 Chuvash / Tchouvache — `cv_cu / Чӑвашла`**.\n- **Do not redo Chuvash.**\n- Next language: **#59**.\n\n## #58 Chuvash verification\n\nStaging branch: `release/0.9.0-chuvash`\n\nOriginal beta base used for staging:\n`aab61dca5f901f26be0cd1c59886c812c1709d07`\n\nFinal build source:\n`74308d879cfe67b8821653ae622fe2917d2e2051`\n\nNeoOrigins coverage:\n- 1.21.1: **2296/2296**\n- 26.1.x: **2307/2307**\n- 26.2: **2307/2307**\n\nStrict QA:\n- missing: **0**\n- overlap: **0**\n- placeholder errors: **0**\n- 10 supported 1.21.1 add-ons: strict success\n- JSON validator: success\n- contextual refinement: success\n- final script sanity: **16,744 Chuvash-specific letters across 29 files**\n\nImportant contextual fixes were made after the initial report exposed false friends: `Origin`, `Power`, On/Off, Minecraft Night Vision (`Ҫӗрлехи куҫ`), Nether (`Незер`), Netherite (`Незерит`), Scales, Pavlov, Apply, Spawn Rules, Loot/Drops, XP, Architect and related UI terms. Do not revert these to raw machine translations.\n\n## Runs and artifacts\n\nBootstrap:\n- run `34379807657`\n- job `102561580556`\n- artifact `10115475171`\n- artifact SHA256 `c3699e4ad25b4ef6cef8128cf2a3bd033b9d05a6390961edb83faebe55303c93`\n\nContextual QA report:\n- run `34380576719`\n- job `102564138958`\n\nRefinement:\n- run `34398767552`\n- job `102625101585`\n\nMetadata:\n- run `34398994850`\n- job `102625846393`\n\nFinal builds — run `34398870533`:\n- 1.21.1 job `102625439066`, artifact `10122670078`, package **27/27**, JAR SHA256 `feb1b1a528ad3735cf3146f9a797f5e2fe3a6cd7bf818892a9ce5958062ff91b`\n- 26.1.x job `102625438886`, artifact `10122652529`, package **17/17**, JAR SHA256 `a95b6a5938ea8c0ea221059f8cf94c467bd18e430b962576035006e6005186b4`\n- 26.2 job `102625438481`, artifact `10122650555`, package **17/17**, JAR SHA256 `6886fd8ab2371c953bcad00135aed29dc586cbd48d86880afd064f840cd1b549`\n\nArtifact ZIP SHA256:\n- 1.21.1 `7481f9e487a82ebac091497e76d7f943496c20e66770c27f7b8a188b3a41049b`\n- 26.1.x `c39180ca5c221f9906f71c33ff830de7be69acc7397486c1ab25ea118f99da42`\n- 26.2 `563d21fcb6c299bef1d6daf677f8609252c2ed8c8782cfc343c057b721de77d5`\n\n## Starting #59\n\nBefore doing anything:\n1. Fetch the exact current HEAD of `release/0.9.0-beta`.\n2. Verify this handoff and `PROJECT_HANDOFF.txt` agree with the current repository state.\n3. Choose a current Minecraft Java locale that is useful, genuinely distinct from the existing 58, and not a near-duplicate regional variant.\n4. Verify official Minecraft/upstream translations before creating fallbacks.\n5. Create the new language staging branch from that exact beta HEAD.\n6. Repeat the full strict generation → contextual QA → build → packaging → documentation → fast-forward cycle.\n\nNever force-push. For integration, refetch beta immediately before moving it, require an ahead-only compare with `behind_by=0`, update the beta ref with `force=false`, then verify beta and staging have exactly the same SHA.\n'''
(ROOT / 'NEXT_CHAT_HANDOFF.md').write_text(next_chat, encoding='utf-8')

print('Chuvash handoffs finalized for 58 languages; NEXT LANGUAGE = 59.')
