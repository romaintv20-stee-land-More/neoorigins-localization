# NeoOrigins Localization — 1.0.0 locale plan

Last updated: 2026-09-11

## Selection rule

For 1.0.0, keep one useful locale per language when regional variants do not provide a meaningfully distinct localization. Keep genuinely distinct languages/dialects and meaningful standardized variants. Exclude joke/gadget locales, fictional/fantasy languages, historical language forms, and redundant regional/script variants when an already-supported locale sufficiently covers them.

The first **83 selected locales are complete**, through Friulian (`fur_it`). Traditional Chinese (`zh_tw`) is language #77, Northern Sami (`se_no`) is language #78, Bavarian (`bar`) is language #79, Brabantian (`brb`) is language #80, Andalusian (`esan`) is language #81, East Franconian (`fra_de`) is language #82, and Friulian (`fur_it`) is language #83.

## Remaining selected locales

There are **30** selected locales remaining for 1.0.0:

1. `go_fr` — Gallo
2. `gv_im` — Manx
3. `haw_us` — Hawaiian
4. `io_en` — Ido
5. `isv` — Interslavic
6. `kab_kab` — Kabyle
7. `ksh` — Kölsch
8. `kw_gb` — Cornish
9. `li_li` — Limburgish
10. `lmo` — Lombard
11. `mi_nz` — Māori
12. `moh_ca` — Mohawk
13. `nah` — Nahuatl
14. `nds_de` — Low German
15. `nuk` — Nuu-chah-nulth
16. `oj_ca` — Ojibwe
17. `ovd` — Elfdalian
18. `pls` — Ngiiwa
19. `pt_pt` — European Portuguese
20. `ry_ua` — Rusyn
21. `sah_sah` — Yakut
22. `scn` — Sicilian
23. `swg` — Swabian
24. `sxu` — Upper Saxon
25. `szl` — Silesian
26. `tok` — Toki Pona
27. `tzo_mx` — Tzotzil
28. `vec_it` — Venetian
29. `vro` — Võro
30. `yi_de` — Yiddish

## Explicitly not selected from the remaining Minecraft locale inventory

Regional/script duplicates and already-covered variants include `be_latn`, `de_at`, `de_ch`, `es_ar`, `es_cl`, `es_ec`, `es_mx`, `es_uy`, `es_ve`, `fr_ca`, `fr_ch`, `hal_ua`, `hn_no`, `nl_be`, `tl_ph`, `val_es`, `zh_hk`, and `zlm_arab`.

English regional/joke variants and special-purpose locales are excluded. Historical or fictional/fantasy locales such as Classical Chinese, Gothic, pre-revolutionary Russian, Quenya and Klingon are also excluded.

## Latest completed work

Language #83 **Friulian (`fur_it`)** is complete and integrated into `release/1.0.0`.

- staging branch: `release/1.0.0-friulian`
- bootstrap run: `34639651015`
- bootstrap commit: `cac1127f9e586298e1ddbf71d7d9b93677db2d29` — 29 locale source files generated with full strict coverage
- source strategy: complete Italian semantic coverage + pinned Minecraft `it_it` ↔ `fur_it` corpus, rejecting unsafe/unaligned pairs and requiring conservative evidence for lexical projection
- bootstrap corpus metrics: 8,557 aligned entries, 928 rejected pairs, 243 unchanged pairs, 6,874 exact Friulian strings, 272 learned word mappings
- bootstrap semantic pools: local Italian fallback pool 1,380 distinct keys across 18 files; 1.21.1 official/merged semantic coverage 2,237/3,549; 26.x 2,180/3,560
- bootstrap dialect sanity: 1,631 Friulian markers across 1,050 marked values
- contextual QA corrected visible Italian leftovers `< Indietro` and `Chiudi` using corpus-attested Friulian forms `< Indaûr` and `Siere`
- safe refinement run: `34641007434` — successful; 3,583 values checked, 2 high-visibility values changed, 1,631 dialect markers retained, zero known unsafe UI leftovers
- safe refinement commit: `f96230d1ecbb023b072f8d5d6d351dee5840ae6f`
- strict NeoOrigins and 10 add-on audits passed; placeholders, JSON and whitespace passed
- build run: `34641157601` — 1.21.1, 26.1.x and 26.2 all successful
- packaged `fur_it` files: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- JAR isolation gates passed for add-ons and version-specific deltas
- metadata run: `34641686116` — successful
- final branch metadata commit: `2c0c753db59026fea6838db352dfcc406da8cd5a`
- native catalog name: `Furlan`
- PR: `#20`
- integration commit: `848057a62b4eccb0a6f0a176a2f8a82b89c7014c`
- catalog/README count: 83 locales

## Next work

Start and finish **language #84: Gallo (`go_fr`)** from the current `release/1.0.0` integration branch.

Low German (`nds_de`) remains selected, but its bootstrap is deferred until a translation path that actually targets Low German is available; the current Google-based bootstrap must not silently substitute Standard German.
