# NeoOrigins Localization — 1.0.0 locale plan

Last updated: 2026-09-14

## Selection rule

For 1.0.0, keep one useful locale per language when regional variants do not provide a meaningfully distinct localization. Keep genuinely distinct languages/dialects and meaningful standardized variants. Exclude joke/gadget locales, fictional/fantasy languages, historical language forms, and redundant regional/script variants when an already-supported locale sufficiently covers them.

The first **88 selected locales are complete and integrated**, through Interslavic (`isv`). Traditional Chinese (`zh_tw`) is language #77, Northern Sami (`se_no`) #78, Bavarian (`bar`) #79, Brabantian (`brb`) #80, Andalusian (`esan`) #81, East Franconian (`fra_de`) #82, Friulian (`fur_it`) #83, Gallo (`go_fr`) #84, Manx (`gv_im`) #85, Hawaiian (`haw_us`) #86, Ido (`io_en`) #87, and Interslavic (`isv`) #88.

## Remaining selected locales

There are **25** selected locales remaining for 1.0.0:

1. `kab_kab` — Kabyle
2. `ksh` — Kölsch
3. `kw_gb` — Cornish
4. `li_li` — Limburgish
5. `lmo` — Lombard
6. `mi_nz` — Māori
7. `moh_ca` — Mohawk
8. `nah` — Nahuatl
9. `nds_de` — Low German
10. `nuk` — Nuu-chah-nulth
11. `oj_ca` — Ojibwe
12. `ovd` — Elfdalian
13. `pls` — Ngiiwa
14. `pt_pt` — European Portuguese
15. `ry_ua` — Rusyn
16. `sah_sah` — Yakut
17. `scn` — Sicilian
18. `swg` — Swabian
19. `sxu` — Upper Saxon
20. `szl` — Silesian
21. `tok` — Toki Pona
22. `tzo_mx` — Tzotzil
23. `vec_it` — Venetian
24. `vro` — Võro
25. `yi_de` — Yiddish

## Explicitly not selected from the remaining Minecraft locale inventory

Regional/script duplicates and already-covered variants include `be_latn`, `de_at`, `de_ch`, `es_ar`, `es_cl`, `es_ec`, `es_mx`, `es_uy`, `es_ve`, `fr_ca`, `fr_ch`, `hal_ua`, `hn_no`, `nl_be`, `tl_ph`, `val_es`, `zh_hk`, and `zlm_arab`.

English regional/joke variants and special-purpose locales are excluded. Historical or fictional/fantasy locales such as Classical Chinese, Gothic, pre-revolutionary Russian, Quenya and Klingon are also excluded.

## Latest completed work

Language #88 **Interslavic (`isv`)** is complete and integrated into `release/1.0.0`.

- staging branch: `release/1.0.0-interslavic`
- successful bootstrap run: `34777502902`
- generated source layout: 16 common NeoOrigins chunks + `neoorigins_isv_121` + shared 26.x deltas + 10 add-ons = 29 `isv` source files
- source strategy: safe manual full values, exact whole-string matches from the pinned Minecraft `en_us` ↔ `isv` corpus, then direct English → Interslavic full-string translation with `salavat/nllb-200-distilled-600M-finetuned-isv_v2` (`eng_Latn` → `isv_Latn`)
- no isolated-word projection; technical/project tokens and placeholders were protected
- successful final refinement run: `34777854565`
- generated translation commit: `f7a79133060eaf4058d4f29ea2aa669839e3ec6f`
- strict JSON, placeholder, source-key, upstream-overlap and protected-token gates passed across all 29 files
- Interslavic is machine-generated and is not described as native-speaker-reviewed
- successful build run: `34893764953`
- packaged `isv` inspection gates: **27** files on 1.21.1, **17** on 26.1.x, **17** on 26.2, with add-on and version-delta isolation verified
- final staging metadata commit: `cd7805cec57dee509680e055980cfeb72418a586`
- metadata final state: 88 supported locales, `isv` present across all 11 projects, native name `Medžuslovjansky`, French README name `Interslave`, fallback namespaces `interslavic_common_glob = neoorigins_isv_common_*` and `interslavic_mc_1_21_1 = neoorigins_isv_121`
- PR: `#25`
- integration merge commit: `b4efe78fe46513a582ce36403cf746625b6dcecb`
- catalog/README count: 88 locales
- public build metadata remains `0.9.0-beta`

## Next work

Start and finish **language #89: Kabyle (`kab_kab`)** from the current `release/1.0.0` integration branch. Use English as the semantic source, inspect the pinned Minecraft `kab_kab` corpus first, and use only a translation path that genuinely targets Kabyle for remaining full strings.

Low German (`nds_de`) remains selected, but its bootstrap is deferred until a translation path that actually targets Low German is available; do not silently substitute Standard German.
