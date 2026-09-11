# NeoOrigins Localization — 1.0.0 locale plan

Last updated: 2026-09-11

## Selection rule

For 1.0.0, keep one useful locale per language when regional variants do not provide a meaningfully distinct localization. Keep genuinely distinct languages/dialects and meaningful standardized variants. Exclude joke/gadget locales, fictional/fantasy languages, historical language forms, and redundant regional/script variants when an already-supported locale sufficiently covers them.

The first 77 selected locales are already translated through Traditional Chinese (`zh_tw`).

## Remaining selected locales

There are **36** selected locales remaining for 1.0.0:

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
28. `se_no` — Northern Sami
29. `swg` — Swabian
30. `sxu` — Upper Saxon
31. `szl` — Silesian
32. `tok` — Toki Pona
33. `tzo_mx` — Tzotzil
34. `vec_it` — Venetian
35. `vro` — Võro
36. `yi_de` — Yiddish

## Explicitly not selected from the remaining Minecraft locale inventory

Regional/script duplicates and already-covered variants include `be_latn`, `de_at`, `de_ch`, `es_ar`, `es_cl`, `es_ec`, `es_mx`, `es_uy`, `es_ve`, `fr_ca`, `fr_ch`, `hal_ua`, `hn_no`, `nl_be`, `tl_ph`, `val_es`, `zh_hk`, and `zlm_arab`.

English regional/joke variants and special-purpose locales are excluded. Historical or fictional/fantasy locales such as Classical Chinese, Gothic, pre-revolutionary Russian, Quenya and Klingon are also excluded.

## Current work

Language #78 is **Northern Sami (`se_no`)** on `release/1.0.0-northern-sami`.

Low German (`nds_de`) remains selected, but its bootstrap is deferred until a translation path that actually targets Low German is available; the current Google-based bootstrap must not silently substitute Standard German.
