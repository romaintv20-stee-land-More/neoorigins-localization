# NEXT CHAT HANDOFF — NeoOrigins Localization

## Source of truth

- Repository: `romaintv20-stee-land-More/neoorigins-localization`
- Current release branch: `release/0.9.0-beta`
- **Do not use `main`**: it is behind.
- Read `PROJECT_HANDOFF.txt` first.
- Completed language count: **63**.
- Last completed language: **#63 Esperanto — `eo_uy / Esperanto`**.
- **Do not redo Esperanto.**
- Next language: **#64**.
- The historical NeoOrigins 2.2.27 gaps in Italian, Polish, Russian, Simplified Chinese, Turkish, Czech and Hungarian were recovered **before #59**; do not treat that recovery as pending.

## #63 Esperanto verification

Staging branch: `release/0.9.0-esperanto`

Original beta base used for staging:
`073908c30b0eb6f4d044db02e2208e4a3929ea16`

Final build source:
`ff46ada079431c58b496b5a423f44d159bde05ac`

NeoOrigins 2.2.27 refs:
- 1.21.1 `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2`
- 26.1.x `aa207ef14cf3b938e28b4081162701953957c1d5`
- 26.2 `511cadcafe3027d2a56b4448652ec9b74e2f3b07`

Coverage:
- 1.21.1: **2296/2296**
- 26.1.x: **2307/2307**
- 26.2: **2307/2307**

Strict QA:
- official Esperanto strings upstream at audited refs: **0** for NeoOrigins and **0** for all 10 supported add-ons
- missing: **0**
- overlap: **0**
- placeholder errors: **0**
- all 10 supported 1.21.1 add-ons: strict success
- JSON validator: success
- contextual refinement: success
- main pass: **406 values across 20/29 files**, **109 guarded keys**
- observed pass: **17 additional corrections across 4 files**, **17 guarded keys**, **5 English-remnant classes cleared**
- final contextual sanity: **3660 lexical markers, 2018 Esperanto diacritics, 103603 Latin characters, 29 files**

Important contextual corrections include canonical `Origin`, `Klaso`, `Povoj`, `Apliki`, `Generaj Reguloj`, `Faligaĵoj`, `Noktvido`, `Blaze-skvamoj`, `Skvamoj`, `Pavlova Reflekso`, and all 64 `Fulmoklavo` hotkeys. Do not revert these to raw machine translations such as `Origino`, `Potencoj`, `Nokta vizio`, `Skaloj/pesiloj`, `Pavloved` or English `Hotkey` labels.

## Runs and artifacts

Bootstrap:
- run `34427693801`
- job `102716316421`
- localization commit `f892066eb8202784997f2c1faa8356f319942a5c`
- artifact `10133339592`
- artifact ZIP SHA256 `262163d18febec0eca0786e77097c100310d61118e0d16c299d23956440a6651`

Contextual refinement:
- final successful run `34428286046`
- job `102718101057`
- artifact `10133478568`
- artifact ZIP SHA256 `d0f20d508e9161beabf664f8e66dc8922aa9b00af7ee5a7f01c8777265e999e2`

Metadata:
- run `34428336352`
- job `102718249903`
- commit `9ad0ea92cfd0626c94515a0d34664301578d65dd`
- catalog locale count **63**

Final builds — run `34428493073`, source `ff46ada079431c58b496b5a423f44d159bde05ac`:
- 1.21.1 job `102718727355`, artifact `10133590817`, package **27/27**, JAR SHA256 `79415d11b7b136965d15327eed20f11329a373f3549c6ddb73c654bd9c59b456`, ZIP SHA256 `80201e09822aa1ea01325c39aa9e4eca905020649aea23d7a0949f9931569638`
- 26.1.x job `102718727302`, artifact `10133580258`, package **17/17**, JAR SHA256 `71769b255590bc7fd63c1bd74a541691567c7acae83054cab930a6a04c8059aa`, ZIP SHA256 `693dee48783edced236b76171a29ce8a0f54f013a8fdc19c99c4b803956b738a`
- 26.2 job `102718727118`, artifact `10133581176`, package **17/17**, JAR SHA256 `b4e6e9fb0f991afbbd2942c324d1ee2f30e435e65c6d2c297cc9e1ed8ca1cca7`, ZIP SHA256 `9f7bdb2e4670a15d95f09b8f9edc78694bcc65055f6b8d4b9347fbf4ec7a6d11`

Packaging semantics:
- 1.21.1: 16 common + `neoorigins_eo_121` + 10 add-ons = **27** Esperanto files
- 26.1.x: 16 common + `neoorigins_26_1` = **17** Esperanto files
- 26.2: 16 common + `neoorigins_26_2` = **17** Esperanto files
- no wrong-version overlays or add-ons leak between targets
- packaged NeoOrigins keysets are exact and duplicate-free

## Start of language #64

1. Refetch `release/0.9.0-beta` and use its exact HEAD as the new staging base.
2. Re-read this file and `PROJECT_HANDOFF.txt`; do not use `main`.
3. Re-audit the current Minecraft Java locale inventory and apply the regional-variant dedup rule. Gallo and Võro may be re-evaluated, but do not force a locale through a backend that cannot meet the quality bar.
4. Verify NeoOrigins and all 10 add-ons for official translations before creating fallbacks.
5. Prefer official upstream strings, translate only missing keys, preserve placeholders exactly, and run contextual QA after machine generation.
6. Require strict NeoOrigins coverage **2296/2296, 2307/2307, 2307/2307**, plus all 10 add-ons, JSON validation and target-aware packaging.
7. Build all three targets and inspect JAR contents before integration.
8. Immediately before integration, refetch beta and staging; require staging `behind_by=0`, fast-forward with `force=false`, then verify both refs are identical.
