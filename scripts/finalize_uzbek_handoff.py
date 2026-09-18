#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / 'PROJECT_HANDOFF.txt'
text = p.read_text(encoding='utf-8')

replacements = {
    '0.9.0 development currently has 58 locales:': '0.9.0 development currently has 59 locales:',
    'af_za, az_az, kn_in, cv_cu.\n\nExpansion order so far:': 'af_za, az_az, kn_in, cv_cu, uz_uz.\n\nExpansion order so far:',
    '- 58: Chuvash / cv_cu\n\nFIFTY-EIGHT IS NOT THE FINAL TARGET.': '- 58: Chuvash / cv_cu\n- 59: Uzbek / uz_uz\n\nFIFTY-NINE IS NOT THE FINAL TARGET.',
    '- catalog.json says 57 supported locales': '- catalog.json says 59 supported locales',
    '- README.md says 57 languages and includes Malay ms_my, Filipino fil_ph, Welsh cy_gb, Irish ga_ie, Scottish Gaelic gd_gb, Armenian hy_am, Georgian ka_ge, Kazakh kk_kz, Mongolian mn_mn, Macedonian mk_mk, Belarusian be_by, Faroese fo_fo, Afrikaans af_za, Azerbaijani az_az and Kannada kn_in': "- README.md says 59 languages and includes the full expansion through Chuvash cv_cu and Uzbek uz_uz",
    '51. NEXT ACTION\n---------------\nNEXT LANGUAGE = language 59.': '52. NEXT ACTION\n---------------\nNEXT LANGUAGE = language 60.',
    '10. Do not stop permanently at 58; language expansion should continue unless Romain changes scope.': '10. Do not stop permanently at 59; language expansion should continue unless Romain changes scope.',
}
for old, new in replacements.items():
    if old not in text:
        raise SystemExit(f'PROJECT_HANDOFF expected text missing: {old!r}')
    text = text.replace(old, new, 1)

legacy_re = re.compile(
    r'IMPORTANT LEGACY COVERAGE FINDING:\n.*?\n\nThe physical namespace neoorigins_226',
    re.S,
)
legacy = '''IMPORTANT LEGACY COVERAGE FINDING — RESOLVED BEFORE LANGUAGE 59:
The full 58-locale audit exposed seven historical locales that were already incomplete before NeoOrigins 2.2.27. This was NOT a 2.2.27 regression. The recovery was completed and integrated before Uzbek (#59): Italian, Polish, Russian, Simplified Chinese, Turkish, Czech and Hungarian are now complete against the adopted 2.2.27 baselines.
- 1.21.1: all seven recovered locales now cover the exact required NeoOrigins keyset.
- 26.1.x: all seven recovered locales now cover the exact required NeoOrigins keyset; the three intentional historical keys retained by Turkish/Czech/Hungarian are compatibility extras inherited from 1.21.1 and were packaging-verified.
- 26.2: all seven recovered locales now cover the exact required NeoOrigins keyset; the same three intentional Turkish/Czech/Hungarian compatibility extras were packaging-verified.
- Strict missing / overlap / placeholder audits passed.
- Real 1.21.1, 26.1.x and 26.2 JAR builds passed, including duplicate-key and packaged-keyset checks.
- Recovery was fast-forwarded into release/0.9.0-beta with force=false before release/0.9.0-uzbek was created.

The physical namespace neoorigins_226'''
text, count = legacy_re.subn(legacy, text, count=1)
if count != 1:
    raise SystemExit('Legacy coverage block not found exactly once')

old_publish = 'Before PUBLISHING 0.9.0, re-check whether NeoOrigins upstream has moved beyond 2.2.27 and re-audit against the final intended reference. Also decide whether to complete the seven legacy partial locales before publication.'
new_publish = 'Before PUBLISHING 0.9.0, re-check whether NeoOrigins upstream has moved beyond 2.2.27 and re-audit against the final intended reference. The seven historical partial locales have already been recovered; do not treat that work as pending.'
if old_publish not in text:
    raise SystemExit('Old publication legacy note missing')
text = text.replace(old_publish, new_publish, 1)

section = '''51. UZBEK 0.9.0 STATUS
------------------------
Uzbek locale: uz_uz / O'zbekcha.
Minecraft Java 26.2 language metadata verified before selection:
- language.code: uzb_UZ
- language.name: O'zbekcha
- language.region: O'zbekiston

Status: COMPLETE FOR THE CURRENT 0.9.0 DEVELOPMENT BASELINE: GENERATED, CONTEXTUALLY REFINED, STRICTLY AUDITED, BUILT, PACKAGING-VERIFIED, AND DOCUMENTED.

Selection rationale:
- Uzbek is a current Minecraft Java locale introduced with the 26.2 language expansion.
- It is a distinct Turkic language, not a regional near-duplicate of the existing 58 locales.
- NeoOrigins 2.2.27 has no official uz_uz file on any of the three supported targets, so a complete low-priority fallback is required.

Staging:
- branch: release/0.9.0-uzbek
- exact beta base used to create staging: 55fd96c10847e5775844fd8c60cd31869367bc37
- final build source SHA: 165ade375054bb3413c1104d43ab1a9705cf10b4

NeoOrigins pinned refs (2.2.27):
- 1.21.1: af467a3bc118f6bbc0970d68f7e03fa631d7e6f2
- 26.1.x: aa207ef14cf3b938e28b4081162701953957c1d5
- 26.2: 511cadcafe3027d2a56b4448652ec9b74e2f3b07

Architecture:
- 16 common namespaces: neoorigins_uz_common_01 through neoorigins_uz_common_16
- 1.21.1 delta namespace: neoorigins_uz_121
- 26.1.x overlay: uz_uz inside neoorigins_26_1
- 26.2 overlay: uz_uz inside neoorigins_26_2
- all 10 supported/licensed add-ons receive uz_uz fallback files on 1.21.1
- Gradle target switch: include_uzbek_121_translations / includeUzbek121Translations

Coverage / strict audits:
- NeoOrigins 1.21.1: 2296 / 2296
- NeoOrigins 26.1.x: 2307 / 2307
- NeoOrigins 26.2: 2307 / 2307
- missing: 0
- overlap: 0
- placeholder errors: 0
- all 10 add-on audits: 0 missing / 0 overlap / 0 placeholder errors
- scripts/validate.py: passed
- bootstrap sanity: 2,736 Uzbek lexical markers and 118,063 Latin characters across 29 uz_uz files

Generation / bootstrap:
- first attempt correctly failed because the translation service duplicated a protected %s in Void Warp; no partial localization commit was accepted
- fragile Void Warp and numbered printf strings were then explicitly protected / manually seeded
- successful bootstrap run: 34404408970
- successful bootstrap job: 102643820338
- bootstrap/audit artifact ID: 10124847581
- bootstrap artifact ZIP SHA256: e72fd17629a914e0a678eb4b854ba94c67fce8db2f95384ae1e85704af3f32f2
- generated NeoOrigins split: 2290 common + 6 / 17 / 17 target-specific keys
- generated Uzbek files: 29 total

Contextual terminology QA:
- deterministic refinement run: 34405017821
- refinement job: 102645798233
- refinement commit: 861b9ebb6ed5398392ffc417a970700775939f31
- refined QA artifact ID: 10124960454
- refined QA artifact ZIP SHA256: de4f3000168e932a72784cc11b02be02ff9c8d353949655e95877ef4767e3de9
- 78 guarded gameplay/UI keys found; 18 / 29 files changed by the refinement pass
- corrected machine false friends included Origin as source/provenance, Boing as boring, Scales as weighing scales, Pavlov wording, and an inverted damage description
- canonical/project terms and Minecraft terminology were guarded, including Origin, Klass, Qobiliyatlar, Tunda ko'rish, Nether, Netherit, Spawn Rules, Drops, XP/tajriba, Origin Architect and 64 normalized hotkeys
- all strict audits and contextual assertions passed again after refinement

Metadata evidence:
- metadata run: 34405172443
- metadata job: 102646304663
- metadata commit: c3bb6f59dc033752f5c888facdcbf4b094148f7d
- catalog.json supported_locale_count = 59
- catalog.json, CATALOG.md and README.md include uz_uz / O'zbekcha / Ouzbek and exact three-version coverage
- catalog metadata records the seven-locale historical recovery as completed before #59

Final build evidence:
- build run: 34405347643
- source SHA: 165ade375054bb3413c1104d43ab1a9705cf10b4
- 1.21.1 job 102646879573: success; packaging 27 / 27 uz_uz files; NeoOrigins 2296 expected / 2296 packaged / 0 duplicates
  - artifact ID 10125122605
  - JAR SHA256 4aa2302d09113b0848ba68061e2e960d7bad2929a2e841df056e18a6afa6af73
  - artifact ZIP SHA256 54bf6d875e58dbfc69854ae07dfd85051b0327a75a3a4d767a8f9437f6c7dbd2
- 26.1.x job 102646879547: success; packaging 17 / 17 uz_uz files; NeoOrigins 2307 expected / 2307 packaged / 0 duplicates
  - artifact ID 10125125703
  - JAR SHA256 99c1ffdc550cfe8cb9cc7a1c397b8a73000f58770c79bf1c0ce441e87b41182f
  - artifact ZIP SHA256 d2439f1d23f06f2b9225003badbd6510401ef83ff24723f2b185d7b2cbf87069
- 26.2 job 102646879215: success; packaging 17 / 17 uz_uz files; NeoOrigins 2307 expected / 2307 packaged / 0 duplicates
  - artifact ID 10125120396
  - JAR SHA256 d623a82bafb9291ae3e2fa37a3fd9d17d0c6b87a86440e58684f8ed0c6924e68
  - artifact ZIP SHA256 6fb6ad0e87aed483d319f539b07f69bfb64d9451fdb462526704474fda45807f

Packaging semantics verified by CI:
- 1.21.1 = 16 common + neoorigins_uz_121 + 10 add-ons = 27; no 26.x Uzbek overlays
- 26.1.x = 16 common + neoorigins_26_1 = 17; no add-ons and no neoorigins_uz_121
- 26.2 = 16 common + neoorigins_26_2 = 17; no add-ons and no neoorigins_uz_121
- packaged NeoOrigins keys are unique and equal the exact required target keyset on all three builds

Integration discipline:
- release/0.9.0-beta must be refetched immediately before integration.
- Only fast-forward release/0.9.0-beta to the exact release/0.9.0-uzbek HEAD when compare shows staging is ahead-only and behind_by=0.
- Never force-push.
- After integration, release/0.9.0-beta and release/0.9.0-uzbek must resolve to the exact same SHA.

NEXT LANGUAGE after Uzbek = language 60.
Re-evaluate the current Minecraft Java locale inventory, choose a useful distinct locale not already in the 59-locale set, verify official upstream assets first, and apply the regional-variant dedup rule before generating fallbacks.

'''
marker = '52. NEXT ACTION\n---------------\nNEXT LANGUAGE = language 60.'
if marker not in text:
    raise SystemExit('Renumbered NEXT ACTION marker missing')
if '51. UZBEK 0.9.0 STATUS' in text:
    raise SystemExit('Uzbek section already present')
text = text.replace(marker, section + marker, 1)
p.write_text(text, encoding='utf-8')

next_chat = '''# NEXT CHAT HANDOFF — NeoOrigins Localization

## Source of truth

- Repository: `romaintv20-stee-land-More/neoorigins-localization`
- Current release branch: `release/0.9.0-beta`
- **Do not use `main`**: it is behind.
- Read `PROJECT_HANDOFF.txt` first.
- Completed language count: **59**.
- Last completed language: **#59 Uzbek / Ouzbek — `uz_uz / O'zbekcha`**.
- **Do not redo Uzbek.**
- Next language: **#60**.
- The historical NeoOrigins 2.2.27 gaps in Italian, Polish, Russian, Simplified Chinese, Turkish, Czech and Hungarian were recovered **before #59**; do not treat that recovery as pending.

## #59 Uzbek verification

Staging branch: `release/0.9.0-uzbek`

Original beta base used for staging:
`55fd96c10847e5775844fd8c60cd31869367bc37`

Final build source:
`165ade375054bb3413c1104d43ab1a9705cf10b4`

Minecraft metadata verified for the current Java 26.2 locale:
- code `uzb_UZ`
- name `O'zbekcha`
- region `O'zbekiston`

NeoOrigins 2.2.27 refs:
- 1.21.1 `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2`
- 26.1.x `aa207ef14cf3b938e28b4081162701953957c1d5`
- 26.2 `511cadcafe3027d2a56b4448652ec9b74e2f3b07`

Coverage:
- 1.21.1: **2296/2296**
- 26.1.x: **2307/2307**
- 26.2: **2307/2307**

Strict QA:
- missing: **0**
- overlap: **0**
- placeholder errors: **0**
- all 10 supported 1.21.1 add-ons: strict success
- JSON validator: success
- contextual refinement: success
- bootstrap sanity: **2,736 Uzbek lexical markers, 118,063 Latin chars, 29 files**

Important contextual corrections after machine-translation review include `Origin`, `Klass`, `Qobiliyatlar`, `Tunda ko'rish`, Nether/Netherit, Spawn Rules, Drops, XP/tajriba, Origin Architect, Scales→`Tangachalar`, Pavlov, Boing, damage-direction semantics and 64 hotkeys. Do not revert these to raw machine translations.

## Runs, commits and artifacts

Bootstrap:
- successful run `34404408970`
- job `102643820338`
- artifact `10124847581`
- artifact ZIP SHA256 `e72fd17629a914e0a678eb4b854ba94c67fce8db2f95384ae1e85704af3f32f2`
- first generation attempt had correctly failed on a duplicated `%s`; the fragile Void Warp string was then protected before the successful run

Contextual refinement:
- run `34405017821`
- job `102645798233`
- commit `861b9ebb6ed5398392ffc417a970700775939f31`
- artifact `10124960454`
- artifact ZIP SHA256 `de4f3000168e932a72784cc11b02be02ff9c8d353949655e95877ef4767e3de9`

Metadata:
- run `34405172443`
- job `102646304663`
- commit `c3bb6f59dc033752f5c888facdcbf4b094148f7d`
- catalog locale count **59**

Final builds — run `34405347643`, source `165ade375054bb3413c1104d43ab1a9705cf10b4`:
- 1.21.1 job `102646879573`, artifact `10125122605`, package **27/27**, JAR SHA256 `4aa2302d09113b0848ba68061e2e960d7bad2929a2e841df056e18a6afa6af73`, ZIP SHA256 `54bf6d875e58dbfc69854ae07dfd85051b0327a75a3a4d767a8f9437f6c7dbd2`
- 26.1.x job `102646879547`, artifact `10125125703`, package **17/17**, JAR SHA256 `99c1ffdc550cfe8cb9cc7a1c397b8a73000f58770c79bf1c0ce441e87b41182f`, ZIP SHA256 `d2439f1d23f06f2b9225003badbd6510401ef83ff24723f2b185d7b2cbf87069`
- 26.2 job `102646879215`, artifact `10125120396`, package **17/17**, JAR SHA256 `d623a82bafb9291ae3e2fa37a3fd9d17d0c6b87a86440e58684f8ed0c6924e68`, ZIP SHA256 `6fb6ad0e87aed483d319f539b07f69bfb64d9451fdb462526704474fda45807f`

The build verifier opened each JAR, merged all Uzbek NeoOrigins files, rejected duplicate keys and required the packaged keyset to equal the exact target English-minus-official set.

## Starting #60

Before doing anything:
1. Refetch the exact current HEAD of `release/0.9.0-beta`.
2. Verify this handoff and `PROJECT_HANDOFF.txt` agree with the repository state.
3. Re-evaluate the current Minecraft Java locale inventory and choose a useful distinct language not already in the 59-locale set; do not assume a locale code.
4. Verify current Minecraft language assets and official NeoOrigins/add-on translations before fallbacks.
5. Create the #60 staging branch from the exact beta HEAD.
6. Repeat generation → official-priority pruning → strict structural audits → contextual QA → three real builds → packaging verification → metadata/handoffs → safe fast-forward.

Never force-push. Immediately before integration, refetch beta, require an ahead-only compare with `behind_by=0`, update beta with `force=false`, then refetch both branches and verify exact identical SHA/state.
'''
(ROOT / 'NEXT_CHAT_HANDOFF.md').write_text(next_chat, encoding='utf-8')

print('Uzbek handoffs finalized for 59 languages; NEXT LANGUAGE = 60.')
