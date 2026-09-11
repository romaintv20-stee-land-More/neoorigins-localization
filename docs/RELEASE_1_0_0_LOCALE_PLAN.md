# NeoOrigins Localization — 1.0.0 locale plan

Last updated: 2026-09-11

## Selection rule

For 1.0.0, keep one useful locale per language when regional variants do not provide a meaningfully distinct localization. Keep genuinely distinct languages/dialects and meaningful standardized variants. Exclude joke/gadget locales, fictional/fantasy languages, historical language forms, and redundant regional/script variants when an already-supported locale sufficiently covers them.

The first **81 selected locales are complete**, through Andalusian (`esan`). Traditional Chinese (`zh_tw`) is language #77, Northern Sami (`se_no`) is language #78, Bavarian (`bar`) is language #79, Brabantian (`brb`) is language #80, and Andalusian (`esan`) is language #81.

## Remaining selected locales

There are **32** selected locales remaining for 1.0.0:

1. `fra_de` — East Franconian
2. `fur_it` — Friulian
3. `go_fr` — Gallo
4. `gv_im` — Manx
5. `haw_us` — Hawaiian
6. `io_en` — Ido
7. `isv` — Interslavic
8. `kab_kab` — Kabyle
9. `ksh` — Kölsch
10. `kw_gb` — Cornish
11. `li_li` — Limburgish
12. `lmo` — Lombard
13. `mi_nz` — Māori
14. `moh_ca` — Mohawk
15. `nah` — Nahuatl
16. `nds_de` — Low German
17. `nuk` — Nuu-chah-nulth
18. `oj_ca` — Ojibwe
19. `ovd` — Elfdalian
20. `pls` — Ngiiwa
21. `pt_pt` — European Portuguese
22. `ry_ua` — Rusyn
23. `sah_sah` — Yakut
24. `scn` — Sicilian
25. `swg` — Swabian
26. `sxu` — Upper Saxon
27. `szl` — Silesian
28. `tok` — Toki Pona
29. `tzo_mx` — Tzotzil
30. `vec_it` — Venetian
31. `vro` — Võro
32. `yi_de` — Yiddish

## Explicitly not selected from the remaining Minecraft locale inventory

Regional/script duplicates and already-covered variants include `be_latn`, `de_at`, `de_ch`, `es_ar`, `es_cl`, `es_ec`, `es_mx`, `es_uy`, `es_ve`, `fr_ca`, `fr_ch`, `hal_ua`, `hn_no`, `nl_be`, `tl_ph`, `val_es`, `zh_hk`, and `zlm_arab`.

English regional/joke variants and special-purpose locales are excluded. Historical or fictional/fantasy locales such as Classical Chinese, Gothic, pre-revolutionary Russian, Quenya and Klingon are also excluded.

## Latest completed work

Language #81 **Andalusian (`esan`)** is complete and integrated into `release/1.0.0`.

- staging branch: `release/1.0.0-andalusian`
- safe refinement commit: `d807b5308b08ea9d1d83f882caa2288a35057172`
- build run: `34635563461` — 1.21.1, 26.1.x and 26.2 all successful
- packaged `esan` files: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- strict NeoOrigins and 10 add-on audits passed
- source strategy: complete Spanish semantic coverage + pinned Minecraft `es_es` ↔ `esan` corpus
- contextual QA caught the false positional mapping `daño` → `de`; safe refinement uses isolated 1-word→1-word alignment with repeated evidence and semantic guards
- metadata run: `34635816552` — successful
- final metadata commit: `c9d1f7aec67e145e90559d79051516fa458a5bf2`
- PR: `#18`
- integration commit: `0876b310cacf29e429308c84abcdbd0b11e5b8b9`
- catalog/README count: 81 locales

## Next work

Start and finish **language #82: East Franconian (`fra_de`)** from the current `release/1.0.0` integration branch.

Low German (`nds_de`) remains selected, but its bootstrap is deferred until a translation path that actually targets Low German is available; the current Google-based bootstrap must not silently substitute Standard German.
