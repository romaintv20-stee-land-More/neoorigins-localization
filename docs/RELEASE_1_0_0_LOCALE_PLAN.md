# NeoOrigins Localization — 1.0.0 locale plan

Last updated: 2026-09-13

## Selection rule

For 1.0.0, keep one useful locale per language when regional variants do not provide a meaningfully distinct localization. Keep genuinely distinct languages/dialects and meaningful standardized variants. Exclude joke/gadget locales, fictional/fantasy languages, historical language forms, and redundant regional/script variants when an already-supported locale sufficiently covers them.

The first **86 selected locales are complete and integrated**, through Hawaiian (`haw_us`). Traditional Chinese (`zh_tw`) is language #77, Northern Sami (`se_no`) is language #78, Bavarian (`bar`) is language #79, Brabantian (`brb`) is language #80, Andalusian (`esan`) is language #81, East Franconian (`fra_de`) is language #82, Friulian (`fur_it`) is language #83, Gallo (`go_fr`) is language #84, Manx (`gv_im`) is language #85, and Hawaiian (`haw_us`) is language #86.

## Remaining selected locales

There are **27** selected locales remaining for 1.0.0:

1. `io_en` — Ido
2. `isv` — Interslavic
3. `kab_kab` — Kabyle
4. `ksh` — Kölsch
5. `kw_gb` — Cornish
6. `li_li` — Limburgish
7. `lmo` — Lombard
8. `mi_nz` — Māori
9. `moh_ca` — Mohawk
10. `nah` — Nahuatl
11. `nds_de` — Low German
12. `nuk` — Nuu-chah-nulth
13. `oj_ca` — Ojibwe
14. `ovd` — Elfdalian
15. `pls` — Ngiiwa
16. `pt_pt` — European Portuguese
17. `ry_ua` — Rusyn
18. `sah_sah` — Yakut
19. `scn` — Sicilian
20. `swg` — Swabian
21. `sxu` — Upper Saxon
22. `szl` — Silesian
23. `tok` — Toki Pona
24. `tzo_mx` — Tzotzil
25. `vec_it` — Venetian
26. `vro` — Võro
27. `yi_de` — Yiddish

## Explicitly not selected from the remaining Minecraft locale inventory

Regional/script duplicates and already-covered variants include `be_latn`, `de_at`, `de_ch`, `es_ar`, `es_cl`, `es_ec`, `es_mx`, `es_uy`, `es_ve`, `fr_ca`, `fr_ch`, `hal_ua`, `hn_no`, `nl_be`, `tl_ph`, `val_es`, `zh_hk`, and `zlm_arab`.

English regional/joke variants and special-purpose locales are excluded. Historical or fictional/fantasy locales such as Classical Chinese, Gothic, pre-revolutionary Russian, Quenya and Klingon are also excluded.

## Latest completed work

Language #86 **Hawaiian (`haw_us`)** is complete and integrated into `release/1.0.0`.

- staging branch: `release/1.0.0-hawaiian`
- successful bootstrap run: `34713396852`
- generated source layout: 16 common NeoOrigins chunks + 1.21.1 delta + shared 26.x deltas + 10 add-ons = 29 `haw_us` source files
- source strategy: complete English semantic coverage, safe manual values, exact matches from the pinned Minecraft `en_us` ↔ `haw_us` corpus, then direct automatic English → Hawaiian translation for remaining strings
- technical tokens/placeholders were protected and official upstream translations retain priority through overlap pruning
- successful final refinement run: `34745528317`
- generated translation commit: `f4a44edf4f51b9aa0cf986cc9f33b00b93aac333`
- strict JSON, placeholder, source-key, upstream-overlap and temporary-marker gates passed across all 29 files
- the locale is machine-generated and is not described as native-speaker-reviewed
- build run: `34747059029` — 1.21.1, 26.1.x and 26.2 all successful
- packaged `haw_us` files were inspected directly from the build artifacts: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- JAR isolation gates passed for add-ons and version-specific deltas
- metadata run: `34747318184` — successful
- final staging metadata commit: `51a74d2f52c560fdccf1d0a97ce5593c8c5588d3`
- metadata final state: 86 supported locales, `haw_us` present across all 11 projects, native catalog name `ʻŌlelo Hawaiʻi`, README label `Hawaïen`, fallback namespaces `hawaiian_common_glob = neoorigins_haw_common_*` and `hawaiian_mc_1_21_1 = neoorigins_haw_121`
- PR: `#23`
- integration commit: `27518a0ee052943a02e959e80438e6c092a463e6`
- catalog/README count: 86 locales
- public build metadata remains `0.9.0-beta`

## Next work

Start and finish **language #87: Ido (`io_en`)** from the current `release/1.0.0` integration branch.

Low German (`nds_de`) remains selected, but its bootstrap is deferred until a translation path that actually targets Low German is available; the current Google-based bootstrap must not silently substitute Standard German.
