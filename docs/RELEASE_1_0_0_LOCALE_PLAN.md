# NeoOrigins Localization — 1.0.0 locale plan

Last updated: 2026-09-11

## Selection rule

For 1.0.0, keep one useful locale per language when regional variants do not provide a meaningfully distinct localization. Keep genuinely distinct languages/dialects and meaningful standardized variants. Exclude joke/gadget locales, fictional/fantasy languages, historical language forms, and redundant regional/script variants when an already-supported locale sufficiently covers them.

The first **78 selected locales are complete**, through Northern Sami (`se_no`). Traditional Chinese (`zh_tw`) is language #77 and Northern Sami (`se_no`) is language #78.

## Remaining selected locales

There are **35** selected locales remaining for 1.0.0:

1. `bar` — Bavarian
2. `brb` — Brabantian
3. `esan` — Andalusian
4. `fra_de` — East Franconian
5. `fur_it` — Friulian
6. `go_fr` — Gallo
7. `gv_im` — Manx
8. `haw_us` — Hawaiian
9. `io_en` — Ido
10. `isv` — Interslavic
11. `kab_kab` — Kabyle
12. `ksh` — Kölsch
13. `kw_gb` — Cornish
14. `li_li` — Limburgish
15. `lmo` — Lombard
16. `mi_nz` — Māori
17. `moh_ca` — Mohawk
18. `nah` — Nahuatl
19. `nds_de` — Low German
20. `nuk` — Nuu-chah-nulth
21. `oj_ca` — Ojibwe
22. `ovd` — Elfdalian
23. `pls` — Ngiiwa
24. `pt_pt` — European Portuguese
25. `ry_ua` — Rusyn
26. `sah_sah` — Yakut
27. `scn` — Sicilian
28. `swg` — Swabian
29. `sxu` — Upper Saxon
30. `szl` — Silesian
31. `tok` — Toki Pona
32. `tzo_mx` — Tzotzil
33. `vec_it` — Venetian
34. `vro` — Võro
35. `yi_de` — Yiddish

## Explicitly not selected from the remaining Minecraft locale inventory

Regional/script duplicates and already-covered variants include `be_latn`, `de_at`, `de_ch`, `es_ar`, `es_cl`, `es_ec`, `es_mx`, `es_uy`, `es_ve`, `fr_ca`, `fr_ch`, `hal_ua`, `hn_no`, `nl_be`, `tl_ph`, `val_es`, `zh_hk`, and `zlm_arab`.

English regional/joke variants and special-purpose locales are excluded. Historical or fictional/fantasy locales such as Classical Chinese, Gothic, pre-revolutionary Russian, Quenya and Klingon are also excluded.

## Latest completed work

Language #78 **Northern Sami (`se_no`)** is complete and integrated into `release/1.0.0`.

- refined source commit before build: `5b2190d7fc0d259ed8cd80f3ab06dc8575dd89f1`
- build workflow source: `c2a009303ee0eba843f7a21a4269a0ac098e4cc9`
- build run: `34590740817` — 1.21.1, 26.1.x and 26.2 all successful
- packaged `se_no` files: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- metadata run: `34591141087` — successful
- PR: `#15`
- integration commit: `af8250dd2a3e122eacdae1812f3089db83637dda`
- catalog/README count: 78 locales

Traditional Chinese (`zh_tw`) metadata was finalized in the same integration because its source/refinement had already been completed before the 1.0.0 branch was created.

## Next work

Language #79 has not started yet. `bar` (Bavarian) is the first remaining locale in the selected queue.

Low German (`nds_de`) remains selected, but its bootstrap is deferred until a translation path that actually targets Low German is available; the current Google-based bootstrap must not silently substitute Standard German.
