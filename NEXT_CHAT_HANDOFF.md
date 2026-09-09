# NEXT CHAT HANDOFF — NeoOrigins Localization

## Source of truth

- Repository: `romaintv20-stee-land-More/neoorigins-localization`
- Current release branch: `release/0.9.0-beta`
- **Do not use `main`**: it is behind.
- Read `PROJECT_HANDOFF.txt` first.
- Completed language count: **58**.
- Last completed language: **#58 Chuvash / Tchouvache — `cv_cu / Чӑвашла`**.
- **Do not redo Chuvash.**
- Next language: **#59**.

## #58 Chuvash verification

Staging branch: `release/0.9.0-chuvash`

Original beta base used for staging:
`aab61dca5f901f26be0cd1c59886c812c1709d07`

Final build source:
`74308d879cfe67b8821653ae622fe2917d2e2051`

NeoOrigins coverage:
- 1.21.1: **2296/2296**
- 26.1.x: **2307/2307**
- 26.2: **2307/2307**

Strict QA:
- missing: **0**
- overlap: **0**
- placeholder errors: **0**
- 10 supported 1.21.1 add-ons: strict success
- JSON validator: success
- contextual refinement: success
- final script sanity: **16,744 Chuvash-specific letters across 29 files**

Important contextual fixes were made after the initial report exposed false friends: `Origin`, `Power`, On/Off, Minecraft Night Vision (`Ҫӗрлехи куҫ`), Nether (`Незер`), Netherite (`Незерит`), Scales, Pavlov, Apply, Spawn Rules, Loot/Drops, XP, Architect and related UI terms. Do not revert these to raw machine translations.

## Runs and artifacts

Bootstrap:
- run `34379807657`
- job `102561580556`
- artifact `10115475171`
- artifact SHA256 `c3699e4ad25b4ef6cef8128cf2a3bd033b9d05a6390961edb83faebe55303c93`

Contextual QA report:
- run `34380576719`
- job `102564138958`

Refinement:
- run `34398767552`
- job `102625101585`

Metadata:
- run `34398994850`
- job `102625846393`

Final builds — run `34398870533`:
- 1.21.1 job `102625439066`, artifact `10122670078`, package **27/27**, JAR SHA256 `feb1b1a528ad3735cf3146f9a797f5e2fe3a6cd7bf818892a9ce5958062ff91b`
- 26.1.x job `102625438886`, artifact `10122652529`, package **17/17**, JAR SHA256 `a95b6a5938ea8c0ea221059f8cf94c467bd18e430b962576035006e6005186b4`
- 26.2 job `102625438481`, artifact `10122650555`, package **17/17**, JAR SHA256 `6886fd8ab2371c953bcad00135aed29dc586cbd48d86880afd064f840cd1b549`

Artifact ZIP SHA256:
- 1.21.1 `7481f9e487a82ebac091497e76d7f943496c20e66770c27f7b8a188b3a41049b`
- 26.1.x `c39180ca5c221f9906f71c33ff830de7be69acc7397486c1ab25ea118f99da42`
- 26.2 `563d21fcb6c299bef1d6daf677f8609252c2ed8c8782cfc343c057b721de77d5`

## Starting #59

Before doing anything:
1. Fetch the exact current HEAD of `release/0.9.0-beta`.
2. Verify this handoff and `PROJECT_HANDOFF.txt` agree with the current repository state.
3. Choose a current Minecraft Java locale that is useful, genuinely distinct from the existing 58, and not a near-duplicate regional variant.
4. Verify official Minecraft/upstream translations before creating fallbacks.
5. Create the new language staging branch from that exact beta HEAD.
6. Repeat the full strict generation → contextual QA → build → packaging → documentation → fast-forward cycle.

Never force-push. For integration, refetch beta immediately before moving it, require an ahead-only compare with `behind_by=0`, update the beta ref with `force=false`, then verify beta and staging have exactly the same SHA.
