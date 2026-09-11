# NeoOrigins Localization — Next Chat Handoff

Last updated: 2026-09-11
Repository: `romaintv20-stee-land-More/neoorigins-localization`
Reference / integration branch: `release/1.0.0`

## Mandatory starting rules

- Read this file, `PROJECT_HANDOFF.txt`, and `docs/RELEASE_1_0_0_LOCALE_PLAN.md` before changing anything. For the current 1.0.0 language-expansion state, this file and the locale plan supersede older 0.9.0 status text still present in `PROJECT_HANDOFF.txt`.
- Use `release/1.0.0` as the source-of-truth integration branch for the ongoing 1.0.0 cycle.
- Preserve upstream-first fallback behavior: official translations always win and fallback overlaps must be pruned.
- Continue each locale through bootstrap, strict audit, contextual QA/refinement, all three pinned builds, JAR inspection, metadata, and integration.
- Automated/generative translation assistance is used; do not describe generated locales as fully native-speaker-reviewed unless a real native review occurred.
- Do not bump the public build metadata from `0.9.0-beta` to final `1.0.0` until the selected locale queue is finished and the final global release gates pass.

## Completed language baseline

The first **83 selected locales are complete and integrated**.

Latest completed languages:
- **#77 Traditional Chinese — `zh_tw / 繁體中文`**
- **#78 Northern Sami — `se_no / Davvisámegiella`**
- **#79 Bavarian — `bar / Boarisch`**
- **#80 Brabantian — `brb / Braobans`**
- **#81 Andalusian — `esan / Andalûh`**
- **#82 East Franconian — `fra_de / Fränggisch`**
- **#83 Friulian — `fur_it / Furlan`**

The catalogue and README are at **83 locales**. There are **30 selected locales remaining** for 1.0.0; the authoritative queue and exclusion policy are in `docs/RELEASE_1_0_0_LOCALE_PLAN.md`.

## Friulian final references

- staging branch: `release/1.0.0-friulian`
- bootstrap run: `34639651015`
- bootstrap job: `103395940394`
- bootstrap commit: `cac1127f9e586298e1ddbf71d7d9b93677db2d29`
- generated source layout: 16 common NeoOrigins chunks + 1.21.1 delta + shared 26.x deltas + 10 add-ons = 29 `fur_it` source files
- source strategy: complete Italian semantic coverage plus pinned Minecraft `it_it` ↔ `fur_it` corpus; empty, placeholder-mismatched, unsupported-script, unchanged-English and poorly aligned unsafe pairs are rejected; exact safe mappings may be reused and word projection requires repeated/dominant evidence
- bootstrap corpus metrics: 8,557 aligned entries, 928 rejected pairs, 243 unchanged pairs, 6,874 exact Friulian strings, 272 learned word mappings
- local Italian fallback pool: 1,380 distinct keys across 18 files
- semantic coverage pools: 1.21.1 official=2,237 / merged=3,549; 26.1 and 26.2 official=2,180 / merged=3,560
- bootstrap dialect sanity: 1,631 lexical markers across 1,050 marked values
- contextual QA found visible Italian leftovers `< Indietro` and `Chiudi`; pinned Friulian Minecraft corpus attests `Indaûr` and `Siere`
- safe refinement run: `34641007434`
- safe refinement job: `103400336402`
- refinement commit: `f96230d1ecbb023b072f8d5d6d351dee5840ae6f`
- refinement result: all 3,583 generated values checked; 2 high-visibility labels corrected; 1,631 dialect markers retained; 0 known unsafe UI leftovers
- strict NeoOrigins audits passed at 2,296/2,296 keys on 1.21.1 and 2,307/2,307 on both 26.x targets; all 10 compatible 1.21.1 add-on audits passed; overlaps and placeholder errors are zero
- build workflow commit: `17857d2e7facab30128dee3d45fa1049fb092e93`
- build run: `34641157601` — successful on all three targets
- build jobs: 1.21.1 `103400840619`, 26.1.x `103400840931`, 26.2 `103400840975`
- packaged Friulian file counts enforced by JAR inspection gates:
  - 1.21.1: 27 (16 common + `neoorigins_fur_121` + 10 add-ons)
  - 26.1.x: 17 (16 common + `neoorigins_26_1`)
  - 26.2: 17 (16 common + `neoorigins_26_2`)
- JAR isolation gates passed: 26.x contain no 1.21.1 add-ons or `neoorigins_fur_121`; each build contains only its proper version delta
- metadata workflow run: `34641686116`
- metadata job: `103402721382`
- final branch metadata commit: `2c0c753db59026fea6838db352dfcc406da8cd5a`
- metadata final state: 83 supported locales, `fur_it` present across all 11 projects, 29 source files, fallback namespaces `friulian_common_glob = neoorigins_fur_common_*` and `friulian_mc_1_21_1 = neoorigins_fur_121`
- native metadata/catalog name: `Furlan`; README French label: `Frioulan`
- integration PR: `#20`
- integration commit on `release/1.0.0`: `848057a62b4eccb0a6f0a176a2f8a82b89c7014c`

Do not redo Friulian, East Franconian, Andalusian, Brabantian, Bavarian, Northern Sami, or Traditional Chinese metadata.

## Current pinned upstream baseline

NeoOrigins 2.2.27:
- 1.21.1: `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2` — 2,296 English keys
- 26.1.x: `aa207ef14cf3b938e28b4081162701953957c1d5` — 2,307 English keys
- 26.2: `511cadcafe3027d2a56b4448652ec9b74e2f3b07` — 2,307 English keys

Pinned Minecraft locale corpus:
- repository: `teaSummer/minecraft-locales`
- ref: `83af272f5a618b287781ee9ce2a48cfc8f47dd61`
- Java locale files: `java/<locale>.json`

The 1.21.1 build also supports the established 10 add-ons; 26.x builds intentionally package NeoOrigins translations only.

## Next task

Start and finish **language #84 — Gallo (`go_fr`)** from the current `release/1.0.0` branch.

Use the full established flow: inspect the pinned `go_fr` Minecraft corpus first, choose a defensible complete semantic source, bootstrap conservatively, run strict audits, perform contextual QA/refinement, build all three targets with JAR isolation checks, finalize metadata to 84, merge, and update this handoff plus the locale plan.

Low German (`nds_de`) remains selected but is explicitly deferred until a translation path that targets Low German rather than silently substituting Standard German is available.
