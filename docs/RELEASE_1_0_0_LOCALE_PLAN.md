# NeoOrigins Localization — 1.0.0 locale plan

Last updated: 2026-09-12

## Selection rule

For 1.0.0, keep one useful locale per language when regional variants do not provide a meaningfully distinct localization. Keep genuinely distinct languages/dialects and meaningful standardized variants. Exclude joke/gadget locales, fictional/fantasy languages, historical language forms, and redundant regional/script variants when an already-supported locale sufficiently covers them.

The first **85 selected locales are complete and integrated**, through Manx (`gv_im`). Traditional Chinese (`zh_tw`) is language #77, Northern Sami (`se_no`) is language #78, Bavarian (`bar`) is language #79, Brabantian (`brb`) is language #80, Andalusian (`esan`) is language #81, East Franconian (`fra_de`) is language #82, Friulian (`fur_it`) is language #83, Gallo (`go_fr`) is language #84, and Manx (`gv_im`) is language #85.

## Remaining selected locales

There are **28** selected locales remaining for 1.0.0:

1. `haw_us` — Hawaiian
2. `io_en` — Ido
3. `isv` — Interslavic
4. `kab_kab` — Kabyle
5. `ksh` — Kölsch
6. `kw_gb` — Cornish
7. `li_li` — Limburgish
8. `lmo` — Lombard
9. `mi_nz` — Māori
10. `moh_ca` — Mohawk
11. `nah` — Nahuatl
12. `nds_de` — Low German
13. `nuk` — Nuu-chah-nulth
14. `oj_ca` — Ojibwe
15. `ovd` — Elfdalian
16. `pls` — Ngiiwa
17. `pt_pt` — European Portuguese
18. `ry_ua` — Rusyn
19. `sah_sah` — Yakut
20. `scn` — Sicilian
21. `swg` — Swabian
22. `sxu` — Upper Saxon
23. `szl` — Silesian
24. `tok` — Toki Pona
25. `tzo_mx` — Tzotzil
26. `vec_it` — Venetian
27. `vro` — Võro
28. `yi_de` — Yiddish

## Explicitly not selected from the remaining Minecraft locale inventory

Regional/script duplicates and already-covered variants include `be_latn`, `de_at`, `de_ch`, `es_ar`, `es_cl`, `es_ec`, `es_mx`, `es_uy`, `es_ve`, `fr_ca`, `fr_ch`, `hal_ua`, `hn_no`, `nl_be`, `tl_ph`, `val_es`, `zh_hk`, and `zlm_arab`.

English regional/joke variants and special-purpose locales are excluded. Historical or fictional/fantasy locales such as Classical Chinese, Gothic, pre-revolutionary Russian, Quenya and Klingon are also excluded.

## Latest completed work

Language #85 **Manx (`gv_im`)** is complete and integrated into `release/1.0.0`.

- staging branch: `release/1.0.0-manx`
- successful bootstrap run: `34644525833`
- bootstrap output commit: `ead920cea662391031261f9191a81af45b8f227b`
- generated source layout: 16 common NeoOrigins chunks + 1.21.1 delta + shared 26.x deltas + 10 add-ons = 29 `gv_im` source files
- source strategy: complete English semantic coverage plus exact matches from pinned Minecraft `en_us` ↔ `gv_im` corpus, then direct machine-generated Manx for remaining strings, with technical-token protection and upstream-first pruning
- isolated-word projection was rejected after unsafe English/Manx hybrids appeared; exact-corpus-only was also rejected because it left most content in English
- Google translation transport was hardened through serialized batching, Web `MkEWBc` RPC plus mobile fallback, Unicode private-use token guards and structural singleton fallback
- refinement run `34708491746` translated 2,711/2,711 direct strings but failed only the high-visibility `Search` terminology check (`Lhig` instead of `Ronsee`)
- `Search` → `Ronsee` was pinned in commit `a0ee0476c2da66d9ef856baf2377a66f9ed0ca0d`
- successful final refinement run: `34709247531`
- generated translation commit: `cace759faa1f2715f0555dcb1d81ffe2ab63fc9c`
- manual inspection confirmed valid JSON, intact placeholders/tokens and no visible PUA marker leakage; the locale remains machine-generated and is not described as native-speaker-reviewed
- strict NeoOrigins and all 10 compatible 1.21.1 add-on audits passed; overlap and placeholder gates are clean
- build run: `34712538683` — 1.21.1, 26.1.x and 26.2 all successful
- packaged `gv_im` files: 27 on 1.21.1, 17 on 26.1.x, 17 on 26.2
- JAR isolation gates passed for add-ons and version-specific deltas
- metadata run: `34713180483` — successful
- final staging metadata commit: `1702ae8a5d6a6a357ecacf2dd7e703ca90e96ee0`
- metadata final state: 85 supported locales, `gv_im` present across all 11 projects, native catalog name `Gaelg`, README label `Mannois`, fallback namespaces `manx_common_glob = neoorigins_gv_common_*` and `manx_mc_1_21_1 = neoorigins_gv_121`
- PR: `#22`
- integration commit: `4389ee8038fc176d4ce31b6ad7195967a4d8cdc3`
- catalog/README count: 85 locales

## Next work

Start and finish **language #86: Hawaiian (`haw_us`)** from the current `release/1.0.0` integration branch.

Low German (`nds_de`) remains selected, but its bootstrap is deferred until a translation path that actually targets Low German is available; the current Google-based bootstrap must not silently substitute Standard German.
