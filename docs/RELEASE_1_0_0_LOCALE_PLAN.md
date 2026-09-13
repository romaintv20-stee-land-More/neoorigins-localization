# NeoOrigins Localization — 1.0.0 locale plan

Last updated: 2026-09-13

## Selection rule

For 1.0.0, keep one useful locale per language when regional variants do not provide a meaningfully distinct localization. Keep genuinely distinct languages/dialects and meaningful standardized variants. Exclude joke/gadget locales, fictional/fantasy languages, historical language forms, and redundant regional/script variants when an already-supported locale sufficiently covers them.

The first **87 selected locales are complete and integrated**, through Ido (`io_en`). Traditional Chinese (`zh_tw`) is language #77, Northern Sami (`se_no`) #78, Bavarian (`bar`) #79, Brabantian (`brb`) #80, Andalusian (`esan`) #81, East Franconian (`fra_de`) #82, Friulian (`fur_it`) #83, Gallo (`go_fr`) #84, Manx (`gv_im`) #85, Hawaiian (`haw_us`) #86, and Ido (`io_en`) #87.

## Remaining selected locales

There are **26** selected locales remaining for 1.0.0:

1. `isv` — Interslavic
2. `kab_kab` — Kabyle
3. `ksh` — Kölsch
4. `kw_gb` — Cornish
5. `li_li` — Limburgish
6. `lmo` — Lombard
7. `mi_nz` — Māori
8. `moh_ca` — Mohawk
9. `nah` — Nahuatl
10. `nds_de` — Low German
11. `nuk` — Nuu-chah-nulth
12. `oj_ca` — Ojibwe
13. `ovd` — Elfdalian
14. `pls` — Ngiiwa
15. `pt_pt` — European Portuguese
16. `ry_ua` — Rusyn
17. `sah_sah` — Yakut
18. `scn` — Sicilian
19. `swg` — Swabian
20. `sxu` — Upper Saxon
21. `szl` — Silesian
22. `tok` — Toki Pona
23. `tzo_mx` — Tzotzil
24. `vec_it` — Venetian
25. `vro` — Võro
26. `yi_de` — Yiddish

## Explicitly not selected from the remaining Minecraft locale inventory

Regional/script duplicates and already-covered variants include `be_latn`, `de_at`, `de_ch`, `es_ar`, `es_cl`, `es_ec`, `es_mx`, `es_uy`, `es_ve`, `fr_ca`, `fr_ch`, `hal_ua`, `hn_no`, `nl_be`, `tl_ph`, `val_es`, `zh_hk`, and `zlm_arab`.

English regional/joke variants and special-purpose locales are excluded. Historical or fictional/fantasy locales such as Classical Chinese, Gothic, pre-revolutionary Russian, Quenya and Klingon are also excluded.

## Latest completed work

Language #87 **Ido (`io_en`)** is complete and integrated into `release/1.0.0`.

- staging branch: `release/1.0.0-ido`
- successful bootstrap run: `34747547429`
- generated source layout: 16 common NeoOrigins chunks + `neoorigins_io_121` + shared 26.x deltas + 10 add-ons = 29 `io_en` source files
- source strategy: safe manual full values, exact matches from the pinned Minecraft `en_us` ↔ `io_en` corpus, then direct English → Ido translation with `Helsinki-NLP/opus-mt-en-mul` and target prefix `>>ido<<`
- no isolated-word projection; technical/project tokens and placeholders were protected
- successful final refinement run: `34771622691`
- generated translation commit: `fc7da509b430c517fc5a5e4d05e8c7d0751162af`
- strict JSON, placeholder, source-key, upstream-overlap and protected-token gates passed across all 29 files
- Ido is machine-generated and is not described as native-speaker-reviewed
- successful build run: `34772475271`
- packaged `io_en` inspection gates: **27** files on 1.21.1, **17** on 26.1.x, **17** on 26.2, with add-on and version-delta isolation verified
- metadata run: `34777236473` — successful
- final staging metadata commit: `dddc9c896bc232044d50e5750d36d466c6e3bc96`
- metadata final state: 87 supported locales, `io_en` present across all 11 projects, native/French name `Ido`, fallback namespaces `ido_common_glob = neoorigins_io_common_*` and `ido_mc_1_21_1 = neoorigins_io_121`
- PR: `#24`
- integration merge commit: `d97d72b298950982fd10f32fd2354dcb210ec4b0`
- catalog/README count: 87 locales
- public build metadata remains `0.9.0-beta`

## Next work

Start and finish **language #88: Interslavic (`isv`)** from the current `release/1.0.0` integration branch. First inspect the pinned Minecraft `isv` corpus and determine a reliable full-string completion path before generating the locale.

Low German (`nds_de`) remains selected, but its bootstrap is deferred until a translation path that actually targets Low German is available; do not silently substitute Standard German.
