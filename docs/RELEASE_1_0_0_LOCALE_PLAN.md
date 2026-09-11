# NeoOrigins Localization — 1.0.0 locale plan

Last updated: 2026-09-11

## Selection rule

For 1.0.0, keep one useful locale per language when regional variants do not provide a meaningfully distinct localization. Keep genuinely distinct languages/dialects and meaningful standardized variants. Exclude joke/gadget locales, fictional/fantasy languages, historical language forms, and redundant regional/script variants when an already-supported locale sufficiently covers them.

The first **79 selected locales are complete**, through Bavarian (`bar`). Traditional Chinese (`zh_tw`) is language #77, Northern Sami (`se_no`) is language #78, and Bavarian (`bar`) is language #79.

## Remaining selected locales

There are **34** selected locales remaining for 1.0.0:

1. `brb` — Brabantian
2. `esan` — Andalusian
3. `fra_de` — East Franconian
4. `fur_it` — Friulian
5. `go_fr` — Gallo
6. `gv_im` — Manx
7. `haw_us` — Hawaiian
8. `io_en` — Ido
9. `isv` — Interslavic
10. `kab_kab` — Kabyle
11. `ksh` — Kölsch
12. `kw_gb` — Cornish
13. `li_li` — Limburgish
14. `lmo` — Lombard
15. `mi_nz` — Māori
16. `moh_ca` — Mohawk
17. `nah` — Nahuatl
18. `nds_de` — Low German
19. `nuk` — Nuu-chah-nulth
20. `oj_ca` — Ojibwe
21. `ovd` — Elfdalian
22. `pls` — Ngiiwa
23. `pt_pt` — European Portuguese
24. `ry_ua` — Rusyn
25. `sah_sah` — Yakut
26. `scn` — Sicilian
27. `swg` — Swabian
28. `sxu` — Upper Saxon
29. `szl` — Silesian
30. `tok` — Toki Pona
31. `tzo_mx` — Tzotzil
32. `vec_it` — Venetian
33. `vro` — Võro
34. `yi_de` — Yiddish

## Explicitly not selected from the remaining Minecraft locale inventory

Regional/script duplicates and already-covered variants include `be_latn`, `de_at`, `de_ch`, `es_ar`, `es_cl`, `es_ec`, `es_mx`, `es_uy`, `es_ve`, `fr_ca`, `fr_ch`, `hal_ua`, `hn_no`, `nl_be`, `tl_ph`, `val_es`, `zh_hk`, and `zlm_arab`.

English regional/joke variants and special-purpose locales are excluded. Historical or fictional/fantasy locales such as Classical Chinese, Gothic, pre-revolutionary Russian, Quenya and Klingon are also excluded.

## Latest completed work

Language #79 **Bavarian (`bar`)** is complete and integrated into `release/1.0.0`.

- staging branch: `release/1.0.0-bavarian`
- final pre-metadata build source: `f6f7d3c1c845a8e4562467b6e74828608ee53c22`
- build run: `34628916718` — 1.21.1, 26.1.x and 26.2 all successful
- packaged `bar` files: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- metadata run: `34631900275` — successful
- final metadata commit: `436af54d19589c3b2c065aa7dd08f1f3fc047546`
- PR: `#16`
- integration commit: `575fe95814490e151d15f2964d4ed00a4ac39e10`
- catalog/README count: 79 locales

## Next work

Start and finish **language #80: Brabantian (`brb`)** from the current `release/1.0.0` integration branch.

Low German (`nds_de`) remains selected, but its bootstrap is deferred until a translation path that actually targets Low German is available; the current Google-based bootstrap must not silently substitute Standard German.
