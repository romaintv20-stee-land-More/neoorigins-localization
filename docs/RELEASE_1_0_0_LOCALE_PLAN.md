# NeoOrigins Localization — 1.0.0 locale plan

Last updated: 2026-09-11

## Selection rule

For 1.0.0, keep one useful locale per language when regional variants do not provide a meaningfully distinct localization. Keep genuinely distinct languages/dialects and meaningful standardized variants. Exclude joke/gadget locales, fictional/fantasy languages, historical language forms, and redundant regional/script variants when an already-supported locale sufficiently covers them.

The first **84 selected locales are complete**, through Gallo (`go_fr`). Traditional Chinese (`zh_tw`) is language #77, Northern Sami (`se_no`) is language #78, Bavarian (`bar`) is language #79, Brabantian (`brb`) is language #80, Andalusian (`esan`) is language #81, East Franconian (`fra_de`) is language #82, Friulian (`fur_it`) is language #83, and Gallo (`go_fr`) is language #84.

## Remaining selected locales

There are **29** selected locales remaining for 1.0.0:

1. `gv_im` — Manx
2. `haw_us` — Hawaiian
3. `io_en` — Ido
4. `isv` — Interslavic
5. `kab_kab` — Kabyle
6. `ksh` — Kölsch
7. `kw_gb` — Cornish
8. `li_li` — Limburgish
9. `lmo` — Lombard
10. `mi_nz` — Māori
11. `moh_ca` — Mohawk
12. `nah` — Nahuatl
13. `nds_de` — Low German
14. `nuk` — Nuu-chah-nulth
15. `oj_ca` — Ojibwe
16. `ovd` — Elfdalian
17. `pls` — Ngiiwa
18. `pt_pt` — European Portuguese
19. `ry_ua` — Rusyn
20. `sah_sah` — Yakut
21. `scn` — Sicilian
22. `swg` — Swabian
23. `sxu` — Upper Saxon
24. `szl` — Silesian
25. `tok` — Toki Pona
26. `tzo_mx` — Tzotzil
27. `vec_it` — Venetian
28. `vro` — Võro
29. `yi_de` — Yiddish

## Explicitly not selected from the remaining Minecraft locale inventory

Regional/script duplicates and already-covered variants include `be_latn`, `de_at`, `de_ch`, `es_ar`, `es_cl`, `es_ec`, `es_mx`, `es_uy`, `es_ve`, `fr_ca`, `fr_ch`, `hal_ua`, `hn_no`, `nl_be`, `tl_ph`, `val_es`, `zh_hk`, and `zlm_arab`.

English regional/joke variants and special-purpose locales are excluded. Historical or fictional/fantasy locales such as Classical Chinese, Gothic, pre-revolutionary Russian, Quenya and Klingon are also excluded.

## Latest completed work

Language #84 **Gallo (`go_fr`)** is complete and integrated into `release/1.0.0`.

- staging branch: `release/1.0.0-gallo`
- successful bootstrap run: `34642158821`
- bootstrap output commit: `3ef631a8c90842e177b595433405d9dc1cac6099`
- generated source layout: 16 common NeoOrigins chunks + 1.21.1 delta + shared 26.x deltas + 10 add-ons = 29 `go_fr` source files
- source strategy: complete French semantic coverage plus the pinned Minecraft `fr_fr` ↔ `go_fr` corpus, with conservative rejection/projection guards and upstream-first pruning
- contextual QA found the unsafe high-visibility projection `Phantom` → `Sebllan`; all 3 affected Phantom values were restored/protected
- successful refinement run: `34642867766`
- refinement commit: `5565fbf7f50670cf28ca0b092c97b2e647b617d1`
- refinement result: 3,583 generated values checked, 3 unsafe Phantom projections corrected, 459 Gallo lexical markers retained
- strict NeoOrigins audits passed at 2,296/2,296 keys on 1.21.1 and 2,307/2,307 on both 26.x targets; all 10 compatible 1.21.1 add-on audits passed; overlap and placeholder gates are clean
- build workflow commit: `34ed82f78e024f1c7901f695f5e2a6612d40bbe9`
- build run: `34643042947` — 1.21.1, 26.1.x and 26.2 all successful
- packaged `go_fr` files: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- JAR isolation gates passed for add-ons and version-specific deltas
- metadata run: `34643884667` — successful
- final branch metadata commit: `593402eb323d5b33b14c0b2f5dd1bab846840467`
- metadata final state: 84 supported locales, `go_fr` present across all 11 projects, native catalog name `Galo`, fallback namespaces `gallo_common_glob = neoorigins_go_common_*` and `gallo_mc_1_21_1 = neoorigins_go_121`
- PR: `#21`
- integration commit: `83a697348e1b8d15741cbe6bb7fe53bd8dc0445c`
- catalog/README count: 84 locales

## Next work

Start and finish **language #85: Manx (`gv_im`)** from the current `release/1.0.0` integration branch.

Low German (`nds_de`) remains selected, but its bootstrap is deferred until a translation path that actually targets Low German is available; the current Google-based bootstrap must not silently substitute Standard German.
