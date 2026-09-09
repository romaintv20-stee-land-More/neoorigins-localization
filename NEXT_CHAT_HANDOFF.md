# NEXT CHAT HANDOFF — NeoOrigins Localization

## Source of truth

- Repository: `romaintv20-stee-land-More/neoorigins-localization`
- Current release branch: `release/0.9.0-beta`
- **Do not use `main`**: it is behind.
- Read `PROJECT_HANDOFF.txt` first.
- Completed language count: **59**.
- Last completed language: **#59 Uzbek / Ouzbek — `uz_uz / O'zbekcha`**.
- **Do not redo Uzbek.**
- Next language: **#60**.
- The historical NeoOrigins 2.2.27 gaps in Italian, Polish, Russian, Simplified Chinese, Turkish, Czech and Hungarian were recovered **before #59**; do not treat that recovery as pending.

## #59 Uzbek verification

Staging branch: `release/0.9.0-uzbek`

Original beta base used for staging:
`55fd96c10847e5775844fd8c60cd31869367bc37`

Final build source:
`165ade375054bb3413c1104d43ab1a9705cf10b4`

Minecraft metadata verified for the current Java 26.2 locale:
- code `uzb_UZ`
- name `O'zbekcha`
- region `O'zbekiston`

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
- bootstrap sanity: **2,736 Uzbek lexical markers, 118,063 Latin chars, 29 files**

Important contextual corrections after machine-translation review include `Origin`, `Klass`, `Qobiliyatlar`, `Tunda ko'rish`, Nether/Netherit, Spawn Rules, Drops, XP/tajriba, Origin Architect, Scales→`Tangachalar`, Pavlov, Boing, damage-direction semantics and 64 hotkeys. Do not revert these to raw machine translations.

## Runs, commits and artifacts

Bootstrap:
- successful run `34404408970`
- job `102643820338`
- artifact `10124847581`
- artifact ZIP SHA256 `e72fd17629a914e0a678eb4b854ba94c67fce8db2f95384ae1e85704af3f32f2`
- first generation attempt had correctly failed on a duplicated `%s`; the fragile Void Warp string was then protected before the successful run

Contextual refinement:
- run `34405017821`
- job `102645798233`
- commit `861b9ebb6ed5398392ffc417a970700775939f31`
- artifact `10124960454`
- artifact ZIP SHA256 `de4f3000168e932a72784cc11b02be02ff9c8d353949655e95877ef4767e3de9`

Metadata:
- run `34405172443`
- job `102646304663`
- commit `c3bb6f59dc033752f5c888facdcbf4b094148f7d`
- catalog locale count **59**

Final builds — run `34405347643`, source `165ade375054bb3413c1104d43ab1a9705cf10b4`:
- 1.21.1 job `102646879573`, artifact `10125122605`, package **27/27**, JAR SHA256 `4aa2302d09113b0848ba68061e2e960d7bad2929a2e841df056e18a6afa6af73`, ZIP SHA256 `54bf6d875e58dbfc69854ae07dfd85051b0327a75a3a4d767a8f9437f6c7dbd2`
- 26.1.x job `102646879547`, artifact `10125125703`, package **17/17**, JAR SHA256 `99c1ffdc550cfe8cb9cc7a1c397b8a73000f58770c79bf1c0ce441e87b41182f`, ZIP SHA256 `d2439f1d23f06f2b9225003badbd6510401ef83ff24723f2b185d7b2cbf87069`
- 26.2 job `102646879215`, artifact `10125120396`, package **17/17**, JAR SHA256 `d623a82bafb9291ae3e2fa37a3fd9d17d0c6b87a86440e58684f8ed0c6924e68`, ZIP SHA256 `6fb6ad0e87aed483d319f539b07f69bfb64d9451fdb462526704474fda45807f`

The build verifier opened each JAR, merged all Uzbek NeoOrigins files, rejected duplicate keys and required the packaged keyset to equal the exact target English-minus-official set.

## Starting #60

Before doing anything:
1. Refetch the exact current HEAD of `release/0.9.0-beta`.
2. Verify this handoff and `PROJECT_HANDOFF.txt` agree with the repository state.
3. Re-evaluate the current Minecraft Java locale inventory and choose a useful distinct language not already in the 59-locale set; do not assume a locale code.
4. Verify current Minecraft language assets and official NeoOrigins/add-on translations before fallbacks.
5. Create the #60 staging branch from the exact beta HEAD.
6. Repeat generation → official-priority pruning → strict structural audits → contextual QA → three real builds → packaging verification → metadata/handoffs → safe fast-forward.

Never force-push. Immediately before integration, refetch beta, require an ahead-only compare with `behind_by=0`, update beta with `force=false`, then refetch both branches and verify exact identical SHA/state.
