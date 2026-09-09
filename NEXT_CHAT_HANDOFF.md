# NEXT CHAT HANDOFF — NeoOrigins Localization

## Source of truth

- Repository: `romaintv20-stee-land-More/neoorigins-localization`
- Current release branch: `release/0.9.0-beta`
- **Do not use `main`**: it is behind.
- Read `PROJECT_HANDOFF.txt` first.
- Completed language count: **62**.
- Last completed language: **#62 Somali — `so_so / Soomaali`**.
- **Do not redo Somali.**
- Next language: **#63**.
- The historical NeoOrigins 2.2.27 gaps in Italian, Polish, Russian, Simplified Chinese, Turkish, Czech and Hungarian were recovered **before #59**; do not treat that recovery as pending.

## #62 Somali verification

Staging branch: `release/0.9.0-somali`

Original beta base used for staging:
`6bd58c02c2b8e543d8497c3ddd852d04eb55ae92`

Final build source:
`4ef3c76ee4eb90410a4290b762f878a904fbeba4`

Minecraft Java 26.2 metadata verified before selection:
- code `som_SO`
- name `Soomaali`
- region `Soomaaliya`

NeoOrigins 2.2.27 refs:
- 1.21.1 `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2`
- 26.1.x `aa207ef14cf3b938e28b4081162701953957c1d5`
- 26.2 `511cadcafe3027d2a56b4448652ec9b74e2f3b07`

Coverage:
- 1.21.1: **2296/2296**
- 26.1.x: **2307/2307**
- 26.2: **2307/2307**

Strict QA:
- official Somali strings upstream at audited refs: **0** for NeoOrigins and **0** for all 10 supported add-ons
- missing: **0**
- overlap: **0**
- placeholder errors: **0**
- all 10 supported 1.21.1 add-ons: strict success
- JSON validator: success
- contextual refinement: success
- refinement changed **395 values across 20/29 files**, with **109 guarded keys**
- final contextual sanity: **4524 lexical markers, 8086 orthographic markers, 121946 Latin characters, 29 files**

Important contextual corrections include canonical `Origin`, `Fasal`, `Awoodaha`, `Dhaqan geli`, `Xeerarka Dhalashada`, `Aragtida Habeenka`, `Qolofyada Blaze`, anatomical `Qolofyo`, `Falcelinta Pavlov`, and all 64 `Furaha Degdegga ah` hotkeys. Do not revert these to raw machine translations.

## Runs and artifacts

Bootstrap:
- first generation run `34413792449` failed only because the translation service altered a Unicode placeholder sentinel; no failed localization output was integrated
- successful run `34413860883`
- job `102674182234`
- artifact `10128350400`
- artifact ZIP SHA256 `da94f6b6f5f3a540e53f8edfcaf24a40da7fda8cef961b895a70c9cff74ad6d8`

Contextual refinement:
- run `34414360770`
- job `102675774018`
- artifact `10128462525`
- artifact ZIP SHA256 `4ef12306f208c8154ca9afe5a4e54f0585e9abce8f378d4d1ec1befb145eaabc`
- 395 values changed across 20/29 files; 109 guarded keys

Metadata:
- run `34414607834`
- job `102676559755`
- commit `523e495f64a90f32cf166fd7f6d87ee2d60dda1a`
- catalog locale count **62**

Final builds — run `34414684602`, source `4ef3c76ee4eb90410a4290b762f878a904fbeba4`:
- 1.21.1 job `102676812909`, artifact `10128628531`, package **27/27**, JAR SHA256 `1380b3b6ca0c2fad4f4ac399fd99858be81360895fdda9cf49b81d955e4ad682`, ZIP SHA256 `92b75187336e45187a12d1848285be8eddae970829dc6f43cd7916d6d79de092`
- 26.1.x job `102676812737`, artifact `10128619805`, package **17/17**, JAR SHA256 `2c25043e0c71aed732445e649f32ba4a825da96bd5f86875083daa8d81673b7a`, ZIP SHA256 `b388eb7155a55945791efac7fd39b7b1ee552915fd19fada0916ed86a18b912e`
- 26.2 job `102676812914`, artifact `10128622615`, package **17/17**, JAR SHA256 `f99577159cc34c22b21f15fec69e4d96569d030c2cca426495ddfa50f4b32c45`, ZIP SHA256 `337e753ed7477f526825468a547412bd2770b351bd034eeb77bc93fdbdecc888`

Packaging semantics:
- 1.21.1: 16 common + `neoorigins_so_121` + 10 add-ons = **27** Somali files
- 26.1.x: 16 common + `neoorigins_26_1` = **17** Somali files
- 26.2: 16 common + `neoorigins_26_2` = **17** Somali files
- no wrong-version overlays or add-ons leak between targets
- packaged NeoOrigins keysets are exact and duplicate-free

## Start of language #63

1. Refetch `release/0.9.0-beta` and use its exact HEAD as the new staging base.
2. Re-read this file and `PROJECT_HANDOFF.txt`; do not use `main`.
3. Re-audit the current Minecraft Java locale inventory and apply the regional-variant dedup rule. Gallo and Võro can be reconsidered, but do not force a locale through a backend that cannot meet the quality bar.
4. Verify NeoOrigins and all 10 add-ons for official translations before creating fallbacks.
5. Prefer official upstream strings, translate only missing keys, preserve placeholders exactly, and run contextual QA after machine generation.
6. Require strict NeoOrigins coverage **2296/2296, 2307/2307, 2307/2307**, plus all 10 add-ons, JSON validation and target-aware packaging.
7. Build all three targets and inspect JAR contents before integration.
8. Immediately before integration, refetch beta and staging; require staging `behind_by=0`, fast-forward with `force=false`, then verify both refs are identical.
