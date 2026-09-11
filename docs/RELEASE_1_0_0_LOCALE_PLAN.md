# NeoOrigins Localization — 1.0.0 locale plan

Last updated: 2026-09-11

## Selection rule

For 1.0.0, keep one useful locale per language when regional variants do not provide a meaningfully distinct localization. Keep genuinely distinct languages/dialects and meaningful standardized variants. Exclude joke/gadget locales, fictional/fantasy languages, historical language forms, and redundant regional/script variants when an already-supported locale sufficiently covers them.

The first **80 selected locales are complete**, through Brabantian (`brb`). Traditional Chinese (`zh_tw`) is language #77, Northern Sami (`se_no`) is language #78, Bavarian (`bar`) is language #79, and Brabantian (`brb`) is language #80.

## Remaining selected locales

There are **33** selected locales remaining for 1.0.0:

1. `esan` — Andalusian
2. `fra_de` — East Franconian
3. `fur_it` — Friulian
4. `go_fr` — Gallo
5. `gv_im` — Manx
6. `haw_us` — Hawaiian
7. `io_en` — Ido
8. `isv` — Interslavic
9. `kab_kab` — Kabyle
10. `ksh` — Kölsch
11. `kw_gb` — Cornish
12. `li_li` — Limburgish
13. `lmo` — Lombard
14. `mi_nz` — Māori
15. `moh_ca` — Mohawk
16. `nah` — Nahuatl
17. `nds_de` — Low German
18. `nuk` — Nuu-chah-nulth
19. `oj_ca` — Ojibwe
20. `ovd` — Elfdalian
21. `pls` — Ngiiwa
22. `pt_pt` — European Portuguese
23. `ry_ua` — Rusyn
24. `sah_sah` — Yakut
25. `scn` — Sicilian
26. `swg` — Swabian
27. `sxu` — Upper Saxon
28. `szl` — Silesian
29. `tok` — Toki Pona
30. `tzo_mx` — Tzotzil
31. `vec_it` — Venetian
32. `vro` — Võro
33. `yi_de` — Yiddish

## Explicitly not selected from the remaining Minecraft locale inventory

Regional/script duplicates and already-covered variants include `be_latn`, `de_at`, `de_ch`, `es_ar`, `es_cl`, `es_ec`, `es_mx`, `es_uy`, `es_ve`, `fr_ca`, `fr_ch`, `hal_ua`, `hn_no`, `nl_be`, `tl_ph`, `val_es`, `zh_hk`, and `zlm_arab`.

English regional/joke variants and special-purpose locales are excluded. Historical or fictional/fantasy locales such as Classical Chinese, Gothic, pre-revolutionary Russian, Quenya and Klingon are also excluded.

## Latest completed work

Language #80 **Brabantian (`brb`)** is complete and integrated into `release/1.0.0`.

- staging branch: `release/1.0.0-brabantian`
- validated build source: `7bd19fa2bebbffd8638333e1845fb57cef653c88`
- build run: `34634057893` — 1.21.1, 26.1.x and 26.2 all successful
- packaged `brb` files: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- strict NeoOrigins and 10 add-on audits passed
- contextual refinements include `Human` → `Mens` and edit UI label → `Beweireke`
- metadata run: `34634337318` — successful
- final metadata commit: `2dc089e9c9330cb923a0128e1fdc38da53858e71`
- PR: `#17`
- integration commit: `7c358f40c6b55af42d9ac1d17c1f8a774e4ce05a`
- catalog/README count: 80 locales

## Next work

Start and finish **language #81: Andalusian (`esan`)** from the current `release/1.0.0` integration branch.

Low German (`nds_de`) remains selected, but its bootstrap is deferred until a translation path that actually targets Low German is available; the current Google-based bootstrap must not silently substitute Standard German.
