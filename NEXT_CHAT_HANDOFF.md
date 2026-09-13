# NeoOrigins Localization — Next Chat Handoff

Last updated: 2026-09-13
Repository: `romaintv20-stee-land-More/neoorigins-localization`
Reference / integration branch: `release/1.0.0`

## Mandatory starting rules

- Read this file, `PROJECT_HANDOFF.txt`, and `docs/RELEASE_1_0_0_LOCALE_PLAN.md` before changing anything. For the current 1.0.0 language-expansion state, this file and the locale plan supersede older 0.9.0 status text still present in `PROJECT_HANDOFF.txt`.
- Use `release/1.0.0` as the source-of-truth integration branch.
- Preserve upstream-first fallback behavior: official translations always win and fallback overlaps must be pruned.
- Work one locale at a time and continue it through bootstrap, strict audit, contextual QA/refinement, all three pinned builds, JAR inspection, metadata, PR, and integration.
- Automated/generative translation assistance is used; never claim native-speaker review unless one actually occurred.
- Do not bump public build metadata from `0.9.0-beta` to final `1.0.0` until the selected locale queue and final global release gates are complete.
- Never use isolated-word projection to build mixed English/target-language sentences. Prefer safe manual full values, exact corpus full-string matches, then direct full automatic translation of remaining English.

## Completed integration baseline

The first **86 selected locales are complete and integrated** into `release/1.0.0`, through **#86 Hawaiian — `haw_us / ʻŌlelo Hawaiʻi`**.

Recent integrated languages:
- #77 Traditional Chinese — `zh_tw / 繁體中文`
- #78 Northern Sami — `se_no / Davvisámegiella`
- #79 Bavarian — `bar / Boarisch`
- #80 Brabantian — `brb / Braobans`
- #81 Andalusian — `esan / Andalûh`
- #82 East Franconian — `fra_de / Fränggisch`
- #83 Friulian — `fur_it / Furlan`
- #84 Gallo — `go_fr / Galo`
- #85 Manx — `gv_im / Gaelg`
- #86 Hawaiian — `haw_us / ʻŌlelo Hawaiʻi`

The catalogue and README are at **86 locales**. There are **27 selected locales remaining** for 1.0.0. The authoritative queue is `docs/RELEASE_1_0_0_LOCALE_PLAN.md`.

Do not redo completed locale metadata.

## Hawaiian #86 — final references

- staging branch: `release/1.0.0-hawaiian`
- bootstrap run: `34713396852` — successful
- pinned Minecraft corpus: `teaSummer/minecraft-locales` at `83af272f5a618b287781ee9ce2a48cfc8f47dd61`
- generated layout: 16 common chunks + `neoorigins_haw_121` + shared 26.x deltas + 10 add-ons = **29 `haw_us` source files**
- completion path: safe manual full values, exact pinned Minecraft Hawaiian full-string matches, then direct English → Hawaiian automatic translation for remaining strings
- direct translation transport: serialized Google Translate Web `MkEWBc` RPC with mobile fallback, adapted from the hardened Manx engine
- technical/project tokens and placeholders are protected with Unicode private-use markers and structural fallback where needed
- no Manx-specific lexical checks or isolated-word projection were used
- successful final refinement run: `34745528317`
- generated translation commit: `f4a44edf4f51b9aa0cf986cc9f33b00b93aac333`
- strict JSON, key, placeholder, overlap, temporary-marker and pipeline-mixing gates passed across all 29 files
- Hawaiian remains machine-generated; no native-speaker review is claimed
- build-trigger commit: `57ed349f7a1fb8a0ee9dd443d9e38e7f07039ba6`
- successful build run: `34747059029`
- built artifacts were downloaded and inspected directly:
  - 1.21.1: **27** `haw_us` files, delta `neoorigins_haw_121`, 10 add-ons present
  - 26.1.x: **17** `haw_us` files, delta `neoorigins_26_1`, no 1.21.1 add-ons
  - 26.2: **17** `haw_us` files, delta `neoorigins_26_2`, no 1.21.1 add-ons
- build workflow restored to manual-only in commit `7a0f024499757bf69aec5970f630037c8e676bcc`
- metadata finalizer run: `34747318184` — successful
- final staging metadata commit: `51a74d2f52c560fdccf1d0a97ce5593c8c5588d3`
- metadata final state: 86 supported locales, `haw_us` across all 11 projects, native catalog name `ʻŌlelo Hawaiʻi`, README French label `Hawaïen`
- Hawaiian fallback namespaces: `hawaiian_common_glob = neoorigins_haw_common_*`; `hawaiian_mc_1_21_1 = neoorigins_haw_121`
- integration PR: `#23`
- integration merge commit: `27518a0ee052943a02e959e80438e6c092a463e6`
- locale-plan advancement commit: `5201cba654fe940252d00e02a2f9b419b9d82121`
- public build version remains `0.9.0-beta`

## Ido #87 — work in progress

- staging branch: `release/1.0.0-ido`
- locale code: `io_en`; native/French name: `Ido`
- pinned Minecraft corpus: `teaSummer/minecraft-locales` at `83af272f5a618b287781ee9ce2a48cfc8f47dd61`, file `java/io_en.json`
- generated source layout: 16 common chunks + `neoorigins_io_121` + shared 26.x deltas + 10 add-ons = **29 `io_en` source files**
- Google Translate is not used as the Ido completion path; the direct model is `Helsinki-NLP/opus-mt-en-mul` (Apache-2.0), target prefix `>>ido<<`
- completion policy: safe manual full values, exact whole-string matches from the pinned Minecraft Ido corpus, then direct full English → Ido OPUS translation; no isolated-word projection
- placeholders and technical/project names are protected and validated; `Origin Architect` is intentionally preserved
- initial refinement run `34769194090`, job `103755546817`, reached **1,440 / 2,704** direct OPUS strings before failing on protected-token spacing: `NeoOrigins Common Configuration` became `NeoOriginsKomunala Configurado`
- root cause was structural fallback stripping whitespace around a protected token, not a language/model failure
- `scripts/refine_ido.py` was fixed to split leading/core/trailing whitespace and reattach it after translating only the natural-language core
- corrected refinement run: **`34771622691`**, job `103762137745`; currently running full OPUS refinement, with bootstrap/discovery/setup steps already green
- Ido build workflow is prepared to auto-run when refined `src/**/io_en.json` files are pushed; it asserts **27 / 17 / 17** and strict version/delta isolation
- metadata-finalization workflow is prepared but its trigger script must only be added after the three builds pass
- public build version remains `0.9.0-beta`

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

Finish **language #87 — Ido (`io_en`)**. First inspect run `34771622691`; if it succeeds, verify the generated commit and automatic 27/17/17 build. If it fails, inspect the exact log and fix automatically. Only after the build passes should Ido metadata be finalized, followed by PR/merge into `release/1.0.0` and locale-plan advancement.

After Ido integration, the next selected locale is **#88 Interslavic (`isv`)**.

Low German (`nds_de`) remains selected but is explicitly deferred until a translation path that targets Low German rather than silently substituting Standard German is available.
