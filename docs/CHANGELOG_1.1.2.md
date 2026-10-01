# NeoOrigins Localization 1.1.2

## Highlights

- Updated **Origins Furries for NeoOrigins** from **1.0.0 to 1.0.3** on Minecraft 1.21.1.
- Added translations for **52 new Origins Furries localization keys**.
- Added those 52 keys to all **93 supported locales**, for **4,836 new fallback entries**.
- Origins Furries coverage is now **169/169 keys** for every supported locale.
- Updated the Origins Furries upstream audit to check all 93 locales.
- Updated project metadata, catalog data and attribution references to the 1.0.3 upstream JAR.

## NeoOrigins compatibility

NeoOrigins **2.2.29** has the same localization payload as 2.2.28 on all supported Minecraft targets, so no additional NeoOrigins translation delta is required.

Verified English key counts remain:

- Minecraft 1.21.1: **2,532 / 2,532**
- Minecraft 26.1.x: **2,536 / 2,536**
- Minecraft 26.2: **2,535 / 2,535**

## Builds

- **1.1.2+1.21.1** — Java 21 — includes NeoOrigins and the supported 1.21.1 add-ons, including Origins Furries 1.0.3.
- **1.1.2+26.1** — Java 25 — NeoOrigins only.
- **1.1.2+26.2** — Java 25 — NeoOrigins only.

The 26.1.x and 26.2 localization payloads are unchanged from 1.1.1; their version numbers are bumped to keep the release synchronized across all three targets.

## Validation

- JSON structure validation.
- Missing-key and overlap audits.
- Placeholder validation.
- Per-target packaging checks.
- Origins Furries 1.0.3 audit across all 93 supported locales.
- Minecraft 1.21.1 / 26.1.x / 26.2 CI builds.

The new translations are machine-assisted and structurally validated. Native-language review is still welcome, especially for regional and low-resource locales.
