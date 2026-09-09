# NeoOrigins Localization — Next Chat Handoff

Last verified: 2026-09-09

> `PROJECT_HANDOFF.txt` remains the authoritative cross-chat source of truth. This file is a compact continuation snapshot for starting the next conversation without reconstructing the previous one.

## Exact current repository state

- Repository: `romaintv20-stee-land-More/neoorigins-localization`
- Active cumulative development branch: `release/0.9.0-beta`
- Current beta HEAD: `4bebe3fb45fa796eda4d5fcfed084d9db4862d5e`
- HEAD commit message: `Finalize Kannada 0.9.0 handoff`
- Current target release: `0.9.0 Beta`
- `main` is behind the cumulative release state and MUST NOT be used as the base for current development.
- `0.8.0 Beta` is already published externally.

## Current language state

The project currently has **57 locales**:

`fr_fr, de_de, es_es, pt_br, nl_nl, it_it, pl_pl, ru_ru, tr_tr, zh_cn, cs_cz, hu_hu, ja_jp, ko_kr, uk_ua, id_id, sv_se, da_dk, fi_fi, no_no, ro_ro, el_gr, bg_bg, vi_vn, ar_sa, he_il, th_th, sk_sk, sl_si, hr_hr, sr_sp, sr_cs, ca_es, et_ee, lt_lt, lv_lv, eu_es, gl_es, hi_in, nn_no, fa_ir, is_is, ms_my, fil_ph, cy_gb, ga_ie, gd_gb, hy_am, ka_ge, kk_kz, mn_mn, mk_mk, be_by, fo_fo, af_za, az_az, kn_in`

Recent expansion order:

- 42 Icelandic `is_is`
- 43 Malay `ms_my`
- 44 Filipino `fil_ph`
- 45 Welsh `cy_gb`
- 46 Irish `ga_ie`
- 47 Scottish Gaelic `gd_gb`
- 48 Armenian `hy_am`
- 49 Georgian `ka_ge`
- 50 Kazakh `kk_kz`
- 51 Mongolian `mn_mn`
- 52 Macedonian `mk_mk`
- 53 Belarusian `be_by`
- 54 Faroese `fo_fo`
- 55 Afrikaans `af_za`
- 56 Azerbaijani `az_az`
- 57 Kannada `kn_in`

**NEXT LANGUAGE = language 58.**

57 is NOT the final target. Continue toward essentially all useful Minecraft Java locales unless Romain explicitly changes scope.

## Important correction from the closed conversation

An intermediate chat state suggested Kannada refinement was still running. That state is OBSOLETE.

Kannada is already **fully finalized and integrated** in `release/0.9.0-beta`. Do not redo Kannada, do not resume run 34377027911 as unfinished, and do not branch from the old 56-language Azerbaijani HEAD.

Start language 58 from the current beta HEAD listed above, after re-reading `PROJECT_HANDOFF.txt` and re-checking the branch HEAD in GitHub because another process may have advanced it.

## Kannada #57 final verified state

Locale: `kn_in / ಕನ್ನಡ`

Status: generated, contextually refined, strictly audited, built, packaging-verified, documented, handoff-finalized, and integrated.

Coverage:

- NeoOrigins 1.21.1: `2296 / 2296`
- NeoOrigins 26.1.x: `2307 / 2307`
- NeoOrigins 26.2: `2307 / 2307`
- all 10 supported 1.21.1 add-ons: complete against established baselines
- strict overlap: `0`
- strict missing: `0`
- placeholder errors: `0`
- JSON validation: passed

Bootstrap:

- branch: `release/0.9.0-kannada`
- workflow: `.github/workflows/bootstrap-kannada.yml`
- run: `34375980559` — SUCCESS
- localization commit: `2c52327192c805d3fafff984f98458e8b3f9c81f` — `Add Kannada localization fallback`
- audit artifact: `10113935206`
- audit artifact SHA256: `fff9418c8fe475b5731db1d92e11fefbbec06269b7fdbf4d31dbb8582950e362`
- NeoOrigins split: 2290 common + 6/17/17 target deltas
- 10 add-on fallback files / 1253 physical strings
- bootstrap sanity: 1,573 Kannada lexical markers and 116,549 Kannada-script characters across 29 `kn_in` files

Contextual refinement:

- workflow: `.github/workflows/refine-kannada.yml`
- first refinement run `34376823511` stopped only on an intentionally strict false-friend guard after all structural audits had already passed
- the remaining `Scales` measuring-scales false friend was corrected without weakening the guard
- final refinement run: `34377027911` — SUCCESS
- final refinement commit: `657e49555bf2f94150cacc2c55843c7545a2efea` — `Refine Kannada Minecraft terminology`
- final sanity: 1,575 Kannada lexical markers and 116,278 Kannada-script characters across 29 source files
- post-refinement NeoOrigins audits: 0 overlap / 0 missing / 0 placeholder errors on all three targets
- all 10 add-on audits: 0 overlap / 0 missing / 0 placeholder errors

Metadata:

- run: `34377471271` — SUCCESS
- commit: `30f4642692743bfa96bf1e341d3a2080fabd80a9` — `Document Kannada localization in 0.9.0 beta`
- `catalog.json`, `CATALOG.md`, and `README.md` declare 57 locales and include `kn_in / ಕನ್ನಡ`

Final Kannada three-target CI:

- workflow: `.github/workflows/build-0.9.0-kannada.yml`
- workflow commit: `611e5fa951ada19ce83c524ad10f16d8f2dc2409`
- run: `34377605054` — SUCCESS on all three jobs

Packaging:

- 1.21.1: exactly 27 `kn_in` files = 16 common + one 1.21.1 delta + 10 add-ons
- 26.1.x: exactly 17 `kn_in` files = 16 common + correct 26.1 delta
- 26.2: exactly 17 `kn_in` files = 16 common + correct 26.2 delta
- no add-on namespace or `neoorigins_kn_121` leaked into 26.x

Final JAR artifacts:

- 1.21.1: artifact `10114557230`, size 4,473,026 bytes, SHA256 `8a211f537a39ef0c8a191eb41a12b6232bddb524e68f715d2c7235477acdb56d`
- 26.1.x: artifact `10114582771`, size 2,431,935 bytes, SHA256 `66c31bd567a78255d4c4c912425e27ee365f1836ea7f94a2ef4ee50d7ddb006e`
- 26.2: artifact `10114546850`, size 2,431,538 bytes, SHA256 `6214331ee1a694ddef8ae8c63035ac958f8ac8584e31764b9c417d5ab5c44d92`

QA caveat: Kannada used automated/generative translation assistance, structural QA and manual contextual refinement. It has not been fully reviewed by a native Kannada speaker. Do not present green CI as native-speaker perfection.

## Project translation rules that must not change

- NeoOrigins is the main translated mod.
- Official upstream translations ALWAYS have priority.
- Fallbacks only fill keys absent upstream.
- If upstream later adds official translations, overlapping fallback keys must be pruned.
- No localization is generated at runtime in Minecraft.
- Automated/generative translation assistance is allowed and heavily used, but must be followed by structural QA and contextual refinement.
- Never claim the translations are fully native-speaker-reviewed unless they actually are.
- Preserve all placeholders such as `%s`, `%d`, `%1$s`, `%2$s`, `%3$s`, `%mm`, `%n`, etc.
- For numbered placeholders, grammatical reordering is allowed; validate the placeholder multiset/sorted set rather than requiring the original order.
- Fragile multi-placeholder death messages should be manually pre-seeded/protected if the translation engine risks corrupting them.
- Placeholder sentinels should use punctuation/digits and restoration should tolerate inserted whitespace; this pattern was necessary for Mongolian/Macedonian and remains the safer architecture.

## Regional/script dedup rule

Do not blindly add every regional duplicate.

- If variants differ only by one/few words, keep one representative.
- Keep separate variants if vocabulary, orthography/script, grammar, terminology, or actual Minecraft usage differs materially.
- Compare current Minecraft locale files for borderline cases.
- Nynorsk `nn_no` intentionally remains separate from Bokmål `no_no`.
- Serbian Cyrillic `sr_sp` and Serbian Latin `sr_cs` intentionally remain separate.

## Current build targets and pinned NeoOrigins references

Targets:

- Minecraft 1.21.1 / Java 21
- Minecraft 26.1.x / Java 25
- Minecraft 26.2 / Java 25

NeoOrigins 2.2.26 references currently used for expansion:

- 1.21.1: `860ecdb24e723983e93004ea8ceb5de90ccf0d70`
- 26.1.x: `3c1c7365507679c836d3c14af5d4dd0654652e87`
- 26.2: `65864716a5a796fa1c51ec3e8a6d9640abebb4ca`

Before publishing 0.9.0, re-check whether NeoOrigins upstream has moved beyond 2.2.26 and re-audit against the final intended reference if necessary.

Typical newly generated full-fallback split:

- 2290 common NeoOrigins keys
- 1.21.1 delta: 6
- 26.1.x delta: 17
- 26.2 delta: 17

Expected effective NeoOrigins coverage:

- 1.21.1: 2296 / 2296
- 26.1.x: 2307 / 2307
- 26.2: 2307 / 2307

## Supported 1.21.1 add-ons

The 1.21.1 build includes NeoOrigins plus exactly these 10 supported/licensed projects:

1. Medieval Origins Revival — 401 / 401
2. ibarn's quartet origins addon — 69 / 69
3. Origins Fantasy for NeoOrigins — 240 / 240
4. Origins: Backgrounds for NeoOrigins — 65 / 65
5. Origins: More Backgrounds for NeoOrigins — 44 / 44 effective = 39 own + 5 shared
6. Origins: Backgrounds ISS for NeoOrigins — 79 / 79 effective = 77 own + 2 shared
7. Origins Furries for NeoOrigins — 117 / 117
8. Origins: Classes Extended for NeoOrigins — 124 / 124
9. Origins: Classes ISS for NeoOrigins — 99 / 99
10. Origin Architect — 22 / 22

26.x intentionally contains NeoOrigins translations only unless compatibility is separately verified.

Special case: Origin Architect already has complete official Romanian coverage, so `assets/originsmodernui/lang/ro_ro.json` must NOT exist in the fallback pack.

Mob Origins is NOT selected for 0.9.0. Do not re-add it unless Romain explicitly changes scope.

## Licensing constraints

- NeoOrigins: MIT
- Medieval Origins Revival: code MIT; assets/docs CC BY 4.0, attribution required
- ibarn addon: MIT
- Origin Architect: MIT
- Extra Origins: All Rights Reserved — do NOT integrate without explicit author permission
- Mob Origins: not selected regardless of license
- DraconicArcher private CurseForge permission received 2026-09-06 permits redistribution of translated localization strings, with attribution + link, for Origins Fantasy, Origins Backgrounds, Origins More Backgrounds, Origins Backgrounds ISS, Origins Furries, Origins Classes Extended and Origins Classes ISS
- that permission does not permit redistribution of code, textures, models, or gameplay assets
- see `docs/ATTRIBUTIONS.md`

## Exact workflow to use for language 58 and later

1. Read `PROJECT_HANDOFF.txt` FIRST.
2. Fetch the current `release/0.9.0-beta` HEAD again; never assume the SHA in this snapshot is still current.
3. Use fresh current Minecraft Java locale data to choose the next useful locale under the dedup rule.
4. Do not choose a locale already in the 57-locale list.
5. Create `release/0.9.0-<language>` from the exact current beta HEAD.
6. Adapt the newest proven bootstrap architecture (Kannada/Azerbaijani/Macedonian/Mongolian are good recent templates depending script/placeholder needs).
7. Discover official upstream coverage for all three NeoOrigins refs and all 10 add-ons before generating fallbacks.
8. Prune official overlaps. Origin Architect audit supports prune behavior.
9. Generate the locale with placeholder protection and a few fragile manual pre-seeds where appropriate.
10. Run strict audits with `--fail-on-overlap --fail-on-missing --fail-on-placeholders`.
11. Validate JSON and language/script sanity.
12. Sample generated output for contextual false friends. Do not trust a green structural audit as linguistic QA.
13. Add a `refine_<language>.py` / workflow when contextual corrections are needed. Typical problem families: Power, Origin, Class, Apply, Drops, Spawn Rules, Ultimine, Nether/Netherite, Night Vision, Charge, Pavlov, Scales, XP/health, canonical Origin names, Origin Architect HUD labels, and glued sentence spacing.
14. Keep strict linguistic guards; if one fails, fix the translation rather than weakening the guard.
15. Update `catalog.json`, `CATALOG.md`, and `README.md`; increment supported locale count from 57 to 58.
16. Run final three-target builds. 1.21.1 must re-audit all 10 add-ons. Verify exact packaging, normally 27/17/17 for a locale with no official add-on overlap.
17. Record run IDs, artifact IDs, sizes and SHA256 digests in `PROJECT_HANDOFF.txt`.
18. Update handoff to say the new count and `NEXT LANGUAGE = language 59`.
19. Before integration, compare beta vs staging. Require staging `ahead`, `behind_by = 0`, and merge-base equal to the exact beta HEAD used as the staging base.
20. Fast-forward `release/0.9.0-beta` with force disabled.
21. Verify the beta HEAD and re-read the final handoff after integration.

## Git/CI race precautions learned during this project

- Do not edit a staging branch while a workflow that commits/pushes to that same branch is running.
- If beta advances in parallel, do NOT force-update it and do NOT overwrite the newer language. Rebase/transplant onto the new beta state and re-run combined validation before integrating.
- Historical language-specific workflows can retrigger after a beta fast-forward because `build.gradle` changed. Do not misinterpret those retriggers as failure of the newly added language; inspect the dedicated final build for the language being integrated.
- If an unexpected/parasite commit is created during preparation, remove it before using the branch as a release base.

## What the next chat should do when Romain says “Continue”

Do not ask which language.

Immediately:

- read `PROJECT_HANDOFF.txt`
- confirm current beta HEAD
- select the next distinct useful current Minecraft Java locale
- treat it as **language #58** unless the repository has advanced since this snapshot
- carry it through generation, contextual QA, strict audits, metadata, all three final builds, handoff update and safe fast-forward integration
- continue beyond #58 afterward unless Romain changes scope
