# NEXT CHAT HANDOFF — NeoOrigins Localization

## Source of truth

- Repository: `romaintv20-stee-land-More/neoorigins-localization`
- Current release branch: `release/0.9.0-beta`
- **Do not use `main`**: it is behind.
- Read `PROJECT_HANDOFF.txt` first.
- Completed language count: **61**.
- Last completed language: **#61 Luxembourgish / Luxembourgeois — `lb_lu / Lëtzebuergesch`**.
- **Do not redo Luxembourgish.**
- Next language: **#62**.
- The historical NeoOrigins 2.2.27 gaps in Italian, Polish, Russian, Simplified Chinese, Turkish, Czech and Hungarian were recovered **before #59**; do not treat that recovery as pending.

## #61 Luxembourgish verification

Staging branch: `release/0.9.0-luxembourgish`

Original beta base used for staging:
`5f24096a3e6dece302dc2a31f254c7c79a5c8617`

Final build source:
`24c15ad7a25dfc49b1ecb9ef412ba9c959f59603`

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
- final contextual sanity: **3433 Luxembourgish lexical markers, 3980 accented letters, 29 files**

Important contextual corrections include canonical `Origin` terminology, `Klass`, `Fäegkeeten`, `Spawn-Reegelen`, Minecraft `Nuechtsiicht` and `Netherit`, `Schuppen`, `Pavlov-Reaktioun`, and 64 normalized `Schnelltast` hotkeys. Do not revert these to raw machine translations such as `Urspronk`, `Hierkonft`, `Muechten`, `Nuecht Visioun`, `Skalen` or `Pavloved`.

## Runs and artifacts

Bootstrap:
- run `34410661769`
- job `102664059776`
- artifact `10127180809`
- artifact ZIP SHA256 `6f627287d08267ee33b83b513cececa0ec4cd5d5a87da07984890784f4ec7451`

Contextual refinement:
- run `34411346403`
- job `102666222361`
- artifact `10127342267`
- artifact ZIP SHA256 `4ad9bcbf2b5bbcb30db51f187b931df93221591bb250f8b39397585c3494b241`
- 419 values changed across 25/29 files; 86 guarded keys

Metadata:
- run `34411488196`
- job `102666643265`
- commit `d31a9a49972bf4549d5bf0b90fc3930c1c5d80f0`
- catalog locale count **61**

Final builds — run `34411581514`, source `24c15ad7a25dfc49b1ecb9ef412ba9c959f59603`:
- 1.21.1 job `102666974306`, artifact `10127486985`, package **27/27**, JAR SHA256 `13a4193011778e243d4003f8f7acfaf3979df5dbc44c64e779abb22da65974c3`, ZIP SHA256 `c5206533df99d25d10d1bc787d87d3efad9c353dbd21d1a917067be30e5ac0ee`
- 26.1.x job `102666974486`, artifact `10127468957`, package **17/17**, JAR SHA256 `1f1f6e49f32c3127b27fe2a795f4a9c958b2173bf3a433058777c93eb7384f4a`, ZIP SHA256 `8172094b25b4fcde7aa2701ba4a863f00e6f2cb5b923d00b08a2905d1bae542a`
- 26.2 job `102666974466`, artifact `10127470282`, package **17/17**, JAR SHA256 `554e1159fbfbc2dba1978976dbc6b9ab60825c86ae252ca26ea055bdb2ef82ec`, ZIP SHA256 `315e33c93a8b107b5c3c74286b3c8d3878df8cbafb66eca8974de0db3e3d1eda`

## Start of language #62

1. Refetch `release/0.9.0-beta` and use its exact HEAD as the new staging base.
2. Re-read this file and `PROJECT_HANDOFF.txt`; do not use `main`.
3. Re-audit the current Minecraft Java locale inventory and apply the regional-variant dedup rule.
4. Verify NeoOrigins and all 10 add-ons for official translations before creating fallbacks.
5. Prefer official upstream strings, translate only missing keys, preserve placeholders exactly, and run contextual QA after machine generation.
6. Require strict NeoOrigins coverage **2296/2296, 2307/2307, 2307/2307**, plus all 10 add-ons, JSON validation and target-aware packaging.
7. Build all three targets and inspect JAR contents before integration.
8. Immediately before integration, refetch beta and staging; require staging `behind_by=0`, fast-forward with `force=false`, then verify both refs are identical.
