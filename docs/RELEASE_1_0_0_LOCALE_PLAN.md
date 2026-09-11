# NeoOrigins Localization — 1.0.0 locale plan

Last updated: 2026-09-11

## Selection rule

For 1.0.0, keep one useful locale per language when regional variants do not provide a meaningfully distinct localization. Keep genuinely distinct languages/dialects and meaningful standardized variants. Exclude joke/gadget locales, fictional/fantasy languages, historical language forms, and redundant regional/script variants when an already-supported locale sufficiently covers them.

The first **82 selected locales are complete**, through East Franconian (`fra_de`). Traditional Chinese (`zh_tw`) is language #77, Northern Sami (`se_no`) is language #78, Bavarian (`bar`) is language #79, Brabantian (`brb`) is language #80, Andalusian (`esan`) is language #81, and East Franconian (`fra_de`) is language #82.

## Remaining selected locales

There are **31** selected locales remaining for 1.0.0:

1. `fur_it` — Friulian
2. `go_fr` — Gallo
3. `gv_im` — Manx
4. `haw_us` — Hawaiian
5. `io_en` — Ido
6. `isv` — Interslavic
7. `kab_kab` — Kabyle
8. `ksh` — Kölsch
9. `kw_gb` — Cornish
10. `li_li` — Limburgish
11. `lmo` — Lombard
12. `mi_nz` — Māori
13. `moh_ca` — Mohawk
14. `nah` — Nahuatl
15. `nds_de` — Low German
16. `nuk` — Nuu-chah-nulth
17. `oj_ca` — Ojibwe
18. `ovd` — Elfdalian
19. `pls` — Ngiiwa
20. `pt_pt` — European Portuguese
21. `ry_ua` — Rusyn
22. `sah_sah` — Yakut
23. `scn` — Sicilian
24. `swg` — Swabian
25. `sxu` — Upper Saxon
26. `szl` — Silesian
27. `tok` — Toki Pona
28. `tzo_mx` — Tzotzil
29. `vec_it` — Venetian
30. `vro` — Võro
31. `yi_de` — Yiddish

## Explicitly not selected from the remaining Minecraft locale inventory

Regional/script duplicates and already-covered variants include `be_latn`, `de_at`, `de_ch`, `es_ar`, `es_cl`, `es_ec`, `es_mx`, `es_uy`, `es_ve`, `fr_ca`, `fr_ch`, `hal_ua`, `hn_no`, `nl_be`, `tl_ph`, `val_es`, `zh_hk`, and `zlm_arab`.

English regional/joke variants and special-purpose locales are excluded. Historical or fictional/fantasy locales such as Classical Chinese, Gothic, pre-revolutionary Russian, Quenya and Klingon are also excluded.

## Latest completed work

Language #82 **East Franconian (`fra_de`)** is complete and integrated into `release/1.0.0`.

- staging branch: `release/1.0.0-east-franconian`
- bootstrap commit: `dccecd0` — 29 locale source files generated with full strict coverage
- safe refinement run: `34638832312` — successful; 526 unsafe/over-aggressive bootstrap projections corrected while preserving 415 dialect markers
- safe refinement commit: `6342645`
- source strategy: complete German semantic coverage + pinned Minecraft `de_de` ↔ `fra_de` corpus with suspicious/untranslated pairs rejected and conservative repeated-evidence lexical projection
- strict NeoOrigins and 10 add-on audits passed; placeholders, JSON and whitespace passed
- build run: `34638996305` — 1.21.1, 26.1.x and 26.2 all successful
- packaged `fra_de` files: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- JAR isolation checks passed for add-ons and version-specific deltas
- metadata run: `34639226494` — successful
- final branch metadata commit: `43dfc1edda0ffca03b15cdb79b1688a676f79220`
- native catalog name: `Fränggisch`
- PR: `#19`
- integration commit: `bbf3d9144b45436300dcd3cd8fe5b43514296f12`
- catalog/README count: 82 locales

## Next work

Start and finish **language #83: Friulian (`fur_it`)** from the current `release/1.0.0` integration branch.

Low German (`nds_de`) remains selected, but its bootstrap is deferred until a translation path that actually targets Low German is available; the current Google-based bootstrap must not silently substitute Standard German.
