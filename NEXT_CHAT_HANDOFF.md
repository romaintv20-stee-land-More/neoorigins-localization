# NEXT CHAT HANDOFF — NeoOrigins Localization

## Source of truth

- Repository: `romaintv20-stee-land-More/neoorigins-localization`
- Current release branch: `release/0.9.0-beta`
- **Do not use `main`**: it is behind.
- Read `PROJECT_HANDOFF.txt` first.
- Completed language count: **60**.
- Last completed language: **#60 Maltese / Maltais — `mt_mt / Malti`**.
- **Do not redo Maltese.**
- Next language: **#61**.
- The historical NeoOrigins 2.2.27 gaps in Italian, Polish, Russian, Simplified Chinese, Turkish, Czech and Hungarian were recovered **before #59**; do not treat that recovery as pending.

## #60 Maltese verification

Staging branch: `release/0.9.0-maltese`

Original beta base used for staging:
`0f6703ced765303ad088077322ec55fd5e02fc00`

Final build source:
`39a3582a22c42295e234c5e15755432025c451b1`

Minecraft Java 26.2 metadata verified before selection:
- code `mlt_MT`
- name `Malti`
- region `Malta`

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
- final contextual sanity: **1688 Maltese lexical markers, 8320 Maltese-specific letters, 29 files**

Important contextual corrections include branded `Origin` terminology, `Klassi`, `Setgħat`, `Applika`, `Regoli tat-Tfaċċar`, `Oġġetti Mwaqqgħin`, official-style `Viżjoni bil-Lejl`, Nether/Netherit, anatomical `Skaldi`, `Reazzjoni ta' Pavlov`, multiple Origins Furries false friends and 64 normalized `Tast Rapidu` hotkeys. Do not revert these to raw machine translations.

Gallo `go_fr` was considered first for #60 because it is a current Minecraft locale, but the current generation backend did not support it cleanly enough for the project's quality bar. This is not a permanent exclusion: re-evaluate Gallo, Võro and the full remaining current Java locale inventory for future languages.

## Runs, commits and artifacts

Bootstrap:
- successful run `34406636751`
- job `102651062952`
- localization commit `c7300873568abb27055fd9bd6f98d41be1fba59b`
- artifact `10125673999`
- artifact ZIP SHA256 `5bd0359ed2f58ccddd72e6bf2404b88c1d6a4641c11560f1023f58ec41cae9c6`

Contextual refinement:
- run `34407239933`
- job `102653050567`
- commit `f8027a0a568436306b8dfe49c80de053bebd3087`
- artifact `10125799887`
- artifact ZIP SHA256 `9632df91f29ed37ccc3b25fb7cf78a29e86e01e8f5785d381413ddda53d64cfa`
- 189 values changed across 20/29 files; 86 guarded keys

Metadata:
- run `34407430131`
- job `102653676489`
- commit `27e214a33031cac3e5c9ed46cbfc7ed68d61b985`
- catalog locale count **60**

Final builds — run `34407512286`, source `39a3582a22c42295e234c5e15755432025c451b1`:
- 1.21.1 job `102653926878`, artifact `10125950371`, package **27/27**, JAR SHA256 `3d2b68ab100b8b5e165c6a3d2b98f57832892a782cdf5f9c2dd36c9a8cd7acb8`, ZIP SHA256 `5d4660b592ad03808dafcf35fe549976ac350f7f7a7afd267df991223ab7b177`
- 26.1.x job `102653926601`, artifact `10125943701`, package **17/17**, JAR SHA256 `5844a019c1880a952d87931c59f5199cc8de15307d8871b9cbc634d9ea156ef5`, ZIP SHA256 `a00972479da98c3942ee4258aa5a7e2710f40632ef1f31699d67f06e99001dc8`
- 26.2 job `102653926923`, artifact `10125933334`, package **17/17**, JAR SHA256 `8bb11b21929a97e35fda0c8922d3369592b47931767620a349052f8b705685b8`, ZIP SHA256 `5f1fb924f42a6677d986427570d978ca140ee6bd3d9b6b8c43a56b0348a965ad`

The build verifier opened each JAR, merged all Maltese NeoOrigins files, rejected duplicate keys and required the packaged keyset to equal the exact target English-minus-official set.

## Starting #61

Before doing anything:
1. Refetch the exact current HEAD of `release/0.9.0-beta`.
2. Verify this handoff and `PROJECT_HANDOFF.txt` agree with the repository state.
3. Re-evaluate the full current Minecraft Java locale inventory and choose a useful distinct language not already in the 60-locale set; do not assume a locale code or that the next candidate must be Gallo.
4. Verify current Minecraft language assets and official NeoOrigins/add-on translations before fallbacks.
5. Create the #61 staging branch from the exact beta HEAD.
6. Repeat generation → official-priority pruning → strict structural audits → contextual QA → three real builds → packaging verification → metadata/handoffs → safe fast-forward.

Never force-push. Immediately before integration, refetch beta, require an ahead-only compare with `behind_by=0`, update beta with `force=false`, then refetch both branches and verify exact identical SHA/state.
