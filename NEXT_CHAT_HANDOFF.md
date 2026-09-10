# NEXT CHAT HANDOFF — NeoOrigins Localization

## Source of truth

- Repository: `romaintv20-stee-land-More/neoorigins-localization`
- Current release branch: `release/0.9.0-beta`
- **Do not use `main`**: it is behind.
- Read `PROJECT_HANDOFF.txt` first.
- Completed language count: **65**.
- Last completed language: **#65 Tamil — `ta_in / தமிழ்`**.
- **Do not redo Tamil.**
- Next language: **#66**.
- The historical NeoOrigins 2.2.27 gaps in Italian, Polish, Russian, Simplified Chinese, Turkish, Czech and Hungarian were recovered before #59; do not treat that recovery as pending.

## #65 Tamil verification

Staging branch: `release/0.9.0-tamil`

Original beta base used for staging:
`3cea648923ed56797976c08a437d6b8e0691bfba`

Final three-target build source:
`1fe618c76fef2eb31c31229924100aca14e207d7`

NeoOrigins 2.2.27 refs:
- 1.21.1 `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2`
- 26.1.x `aa207ef14cf3b938e28b4081162701953957c1d5`
- 26.2 `511cadcafe3027d2a56b4448652ec9b74e2f3b07`

Coverage:
- 1.21.1: **2296/2296**
- 26.1.x: **2307/2307**
- 26.2: **2307/2307**

Strict QA:
- official Tamil strings upstream at audited refs: **0** for NeoOrigins and **0** for all 10 supported add-ons
- missing: **0**
- overlap: **0**
- placeholder errors: **0**
- all 10 supported 1.21.1 add-ons: strict success
- JSON validator: success
- contextual refinement: success
- final sanity: **29 files, 125,382 Tamil-script characters**
- intentional Latin-only values: `JSON`, `NeoOrigins`, `Origin`, `Origin Architect`
- final English/contextual-remnant guard: success
- official Minecraft Tamil terminology used in cleanup includes `இரவு பார்வை` for Night Vision and `அழுகிய சதை` for Rotten Flesh

## Final build run and artifacts

Run `34452266217`, source `1fe618c76fef2eb31c31229924100aca14e207d7`: all three jobs succeeded.

- 1.21.1 job `102790466252`, artifact `10142050230`, package **27/27**, JAR SHA256 `231686076894b26663d9f0373c4b3c47ebed6d72ebb63903e787ce92645fec69`, ZIP SHA256 `57c73642ac86fb409c36134245ff939662d10b6187bad9710be8f34c17c62735`
- 26.1.x job `102790465990`, artifact `10142041119`, package **17/17**, JAR SHA256 `11c47ef075604fc5a4024e8c268a3503581d28d46da9185be0bce7d1cbaa4839`, ZIP SHA256 `dda833380593609d5b7d5496c30716037de733f8a47347646f1a916fc05aa552`
- 26.2 job `102790466194`, artifact `10142057119`, package **17/17**, JAR SHA256 `a766230b80011bda25e92a5312d0997a995570e14becfb5a89d22331bc4babf1`, ZIP SHA256 `b10e229c8b44913660b5507fb30af64b3193ffd0d30a61a8bb2437288e493104`

Packaging semantics:
- 1.21.1: 16 common + `neoorigins_ta_121` + 10 add-ons = **27** Tamil files
- 26.1.x: 16 common + `neoorigins_26_1` = **17** Tamil files
- 26.2: 16 common + `neoorigins_26_2` = **17** Tamil files
- no wrong-version overlays or add-ons leak between targets
- packaged NeoOrigins keysets are exact and duplicate-free

## Start of language #66

1. Refetch `release/0.9.0-beta` and use its exact HEAD as the new staging base.
2. Re-read this file and `PROJECT_HANDOFF.txt`; do not use `main`.
3. Re-audit the current Minecraft Java locale inventory and apply the regional-variant dedup rule.
4. Verify NeoOrigins and all 10 add-ons for official translations before creating fallbacks.
5. Prefer official upstream strings, translate only missing keys, preserve placeholders exactly, and run contextual QA after machine generation.
6. Require strict NeoOrigins coverage **2296/2296, 2307/2307, 2307/2307**, plus all 10 add-ons, JSON validation and target-aware packaging.
7. Build all three targets and inspect JAR contents before integration.
8. Immediately before integration, refetch beta and staging; require staging to be ahead-only / `behind_by=0`, fast-forward with `force=false`, then verify both refs are identical.
