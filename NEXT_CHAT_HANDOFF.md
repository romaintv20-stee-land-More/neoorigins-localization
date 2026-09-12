# NeoOrigins Localization — Next Chat Handoff

Last updated: 2026-09-12
Repository: `romaintv20-stee-land-More/neoorigins-localization`
Reference / integration branch: `release/1.0.0`

## Mandatory starting rules

- Read this file, `PROJECT_HANDOFF.txt`, and `docs/RELEASE_1_0_0_LOCALE_PLAN.md` before changing anything. For the current 1.0.0 language-expansion state, this file and the locale plan supersede older 0.9.0 status text still present in `PROJECT_HANDOFF.txt`.
- Use `release/1.0.0` as the source-of-truth integration branch for the ongoing 1.0.0 cycle.
- Preserve upstream-first fallback behavior: official translations always win and fallback overlaps must be pruned.
- Continue each locale through bootstrap, strict audit, contextual QA/refinement, all three pinned builds, JAR inspection, metadata, and integration.
- Automated/generative translation assistance is used; do not describe generated locales as fully native-speaker-reviewed unless a real native review occurred.
- Do not bump the public build metadata from `0.9.0-beta` to final `1.0.0` until the selected locale queue is finished and the final global release gates pass.

## Completed integration baseline

The first **84 selected locales are integrated** into `release/1.0.0`, through **#84 Gallo — `go_fr / Galo`**.

Recent integrated languages:
- **#77 Traditional Chinese — `zh_tw / 繁體中文`**
- **#78 Northern Sami — `se_no / Davvisámegiella`**
- **#79 Bavarian — `bar / Boarisch`**
- **#80 Brabantian — `brb / Braobans`**
- **#81 Andalusian — `esan / Andalûh`**
- **#82 East Franconian — `fra_de / Fränggisch`**
- **#83 Friulian — `fur_it / Furlan`**
- **#84 Gallo — `go_fr / Galo`**

Gallo integration PR: `#21`; integration commit: `83a697348e1b8d15741cbe6bb7fe53bd8dc0445c`.

Do not redo Gallo, Friulian, East Franconian, Andalusian, Brabantian, Bavarian, Northern Sami, or Traditional Chinese metadata.

## Manx #85 — staging complete, integration pending

- staging branch: `release/1.0.0-manx`
- bootstrap run: `34644525833` — successful
- bootstrap translation commit: `ead920cea662391031261f9191a81af45b8f227b`
- pinned Minecraft corpus: `teaSummer/minecraft-locales` at `83af272f5a618b287781ee9ce2a48cfc8f47dd61`
- corpus metrics: 1,778 aligned entries, 3 rejected pairs, 118 unchanged English pairs, 1,542 exact Manx strings, 9 ambiguous exact sources, 43 reusable isolated-word mappings
- generated layout: 16 common chunks + `neoorigins_gv_121` + shared 26.x deltas + 10 add-ons = 29 `gv_im` source files
- isolated-word projection was rejected after producing unsafe English/Manx hybrids such as `Aquatic Bieauid`; exact-corpus-only was also rejected because it remained overwhelmingly English
- completion path: exact pinned Minecraft Manx corpus matches first, then direct English → Manx machine translation; technical tokens/placeholders are protected; output is not native-speaker-reviewed
- initial direct Google endpoint run `34645108619` failed on HTTP 429
- serialized batching still met first-request throttling; translation transport was switched to Google Translate Web `MkEWBc` RPC with mobile-page fallback
- wrapper/core split fixed empty-string handling; Unicode private-use marker protection was added for technical tokens
- structural singleton fallback commit: `50b9756405790797169123fc20991a2da40d1d69`; on structural validation failure, only natural-language spans are translated and exact technical tokens are spliced back before placeholder revalidation
- refinement run `34708491746` translated all **2,711/2,711** direct strings and then failed only the high-visibility UI sanity check because `Search` became `Lhig`
- manual UI pin commit: `a0ee0476c2da66d9ef856baf2377a66f9ed0ca0d`, pinning `Search` → `Ronsee`
- successful final refinement run: `34709247531`, job `103594845895`
- generated translation commit: `cace759faa1f2715f0555dcb1d81ffe2ab63fc9c`
- high-visibility QA passed: `Reaghey`, `Sauail`, `Ronsee`, with `Origin Architect` intentionally preserved
- manual inspection confirmed valid JSON, intact placeholders/tokens and no visible PUA marker leakage; linguistic quality remains machine-generated and may be anglicized
- Manx build workflow: `.github/workflows/build-1.0.0-manx.yml`
- successful build run: `34712538683`
- JAR inspection results:
  - 1.21.1: **27** `gv_im` files, delta `neoorigins_gv_121`
  - 26.1.x: **17** `gv_im` files, delta `neoorigins_26_1`
  - 26.2: **17** `gv_im` files, delta `neoorigins_26_2`
- JAR isolation gates passed: 26.x contain no 1.21.1 add-ons or `neoorigins_gv_121`; each build contains only its proper version delta
- metadata workflow: `.github/workflows/finalize-1.0.0-locale-85.yml`
- metadata run: `34713180483`, job `103605543525` — successful
- final staging metadata commit: `1702ae8a5d6a6a357ecacf2dd7e703ca90e96ee0`
- metadata final state on staging: **85 supported locales**, `gv_im` present across all 11 projects, 29 source files, native catalog name `Gaelg`, README label `Mannois`, fallback namespaces `manx_common_glob = neoorigins_gv_common_*` and `manx_mc_1_21_1 = neoorigins_gv_121`
- public build version remains `0.9.0-beta`
- next action: integrate `release/1.0.0-manx` into `release/1.0.0`, record PR/merge commit, then update this handoff and the locale plan to 85 integrated / 28 remaining

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

Integrate **language #85 — Manx (`gv_im`)** from `release/1.0.0-manx` into `release/1.0.0` without rerunning its completed bootstrap/refinement/build/metadata work.

Immediately after Manx integration, continue with **language #86 — Hawaiian (`haw_us`)** from the updated `release/1.0.0` branch.

Low German (`nds_de`) remains selected but is explicitly deferred until a translation path that targets Low German rather than silently substituting Standard German is available.
