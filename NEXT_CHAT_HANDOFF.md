# NeoOrigins Localization — Next Chat Handoff

Last updated: 2026-09-13
Repository: `romaintv20-stee-land-More/neoorigins-localization`
Reference / integration branch: `release/1.0.0`

## Mandatory starting rules

- Read this file, `PROJECT_HANDOFF.txt`, and `docs/RELEASE_1_0_0_LOCALE_PLAN.md` before changing anything.
- Use `release/1.0.0` as the source-of-truth integration branch.
- Preserve upstream-first fallback behavior: official translations always win and fallback overlaps must be pruned.
- Work one locale at a time through bootstrap, strict audit, contextual QA/refinement, all three pinned builds, JAR inspection, metadata, PR, and integration.
- Automated/generative translation assistance is used; never claim native-speaker review unless one actually occurred.
- Do not bump public build metadata from `0.9.0-beta` to final `1.0.0` until the selected locale queue and final global release gates are complete.
- Never use isolated-word projection to build mixed English/target-language sentences. Prefer safe manual full values, exact corpus full-string matches, then direct full automatic translation of remaining English.

## Completed integration baseline

The first **87 selected locales are complete and integrated** into `release/1.0.0`, through **#87 Ido — `io_en / Ido`**.

Recent integrated languages:
- #83 Friulian — `fur_it / Furlan`
- #84 Gallo — `go_fr / Galo`
- #85 Manx — `gv_im / Gaelg`
- #86 Hawaiian — `haw_us / ʻŌlelo Hawaiʻi`
- #87 Ido — `io_en / Ido`

The catalogue and README are at **87 locales**. There are **26 selected locales remaining** for 1.0.0. The authoritative queue is `docs/RELEASE_1_0_0_LOCALE_PLAN.md`.

## Ido #87 — final references

- staging branch: `release/1.0.0-ido`
- bootstrap run: `34747547429` — successful
- final refinement run: `34771622691` — successful
- generated translation commit: `fc7da509b430c517fc5a5e4d05e8c7d0751162af`
- build run: `34772475271` — successful, **27 / 17 / 17** `io_en` files
- metadata run: `34777236473` — successful
- final metadata commit: `dddc9c896bc232044d50e5750d36d466c6e3bc96`
- integration PR: `#24`
- integration merge commit: `d97d72b298950982fd10f32fd2354dcb210ec4b0`
- locale-plan advancement commit: `500ad7a498c6328e22f0a32e8168165a3c6e2c0d`
- Ido remains machine-generated; no native-speaker review is claimed

## Interslavic #88 — current staging state

- staging branch: `release/1.0.0-interslavic`
- locale: `isv`; native metadata name prepared as `Medžuslovjansky`; French README name prepared as `Interslave`
- pinned Minecraft corpus: `teaSummer/minecraft-locales` at `83af272f5a618b287781ee9ce2a48cfc8f47dd61`, file `java/isv.json`
- corpus metrics observed in refinement log: **8,556 aligned entries**, **11 rejected pairs**, **1,947 unchanged English pairs**, **6,152 exact Interslavic strings**, **86 ambiguous exact sources**
- bootstrap strategy: English semantic source, safe manual full values, exact whole-string Minecraft corpus matches only; no isolated-word projection
- bootstrap run: `34777502902` — successful
- generated bootstrap commit: `27176400b337d814a51e9bfda4b1a24f7980578e`
- bootstrap structure: **29 `isv` source files** = 16 common chunks + `neoorigins_isv_121` + two 26.x deltas + 10 add-ons
- refinement model: `salavat/nllb-200-distilled-600M-finetuned-isv_v2`, direct `eng_Latn` → `isv_Latn`
- refinement pool: **2,734 unique source strings**; **33 manual/corpus hits**; **2,701 direct full-string NLLB translations**
- first refinement run `34777652053` failed before committing translations because the model glued protected token `HP` to the following translated word (`HPIz`)
- structural fallback was corrected in commit `ac43305102fd1a359976a60be230dbedb1921b0c` to preserve punctuation/numeric affixes around protected tokens while translating only natural-language cores
- corrected refinement run: `34777854565` — currently running; do not treat it as successful until completed and logs/checks are inspected
- build workflow already prepared: `.github/workflows/build-1.0.0-interslavic.yml`; it will trigger only when refined `isv.json` files are pushed and asserts **27 / 17 / 17**, correct deltas and 26.x add-on isolation
- metadata finalizer prepared: `scripts/finalize_interslavic_metadata.py`; target count **88**, 11 project entries, fallback namespaces `interslavic_common_glob = neoorigins_isv_common_*` and `interslavic_mc_1_21_1 = neoorigins_isv_121`
- successful build workflow is configured to run metadata finalization only after all three matrix builds pass
- standalone metadata workflow remains manual-only as a fallback
- Interslavic remains machine-generated; do not claim native-speaker review

## Current pinned upstream baseline

NeoOrigins 2.2.27:
- 1.21.1: `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2` — 2,296 English keys
- 26.1.x: `aa207ef14cf3b938e28b4081162701953957c1d5` — 2,307 English keys
- 26.2: `511cadcafe3027d2a56b4448652ec9b74e2f3b07` — 2,307 English keys

Pinned Minecraft locale corpus:
- repository: `teaSummer/minecraft-locales`
- ref: `83af272f5a618b287781ee9ce2a48cfc8f47dd61`
- Java locale files: `java/<locale>.json`

The 1.21.1 build supports the established 10 add-ons; 26.x builds intentionally package NeoOrigins translations only.

## Next task

Continue corrected Interslavic refinement run `34777854565`. If it fails, inspect the exact translation/QA error and fix automatically. If green, inspect representative `isv` output quality and leakage, verify the automatic **27 / 17 / 17** build plus metadata finalization, restore staging workflows to manual-only where appropriate, finalize this handoff, create/merge the PR into `release/1.0.0`, advance the locale plan to **#89 Kabyle (`kab_kab`)**, and continue.

Low German (`nds_de`) remains selected but explicitly deferred until a translation path that genuinely targets Low German is available.
