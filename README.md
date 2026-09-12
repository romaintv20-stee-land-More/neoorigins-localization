# NeoOrigins Localization

Mod client NeoForge fournissant des **traductions complémentaires en priorité basse** pour NeoOrigins et des add-ons compatibles. Une traduction officielle amont garde toujours la priorité ; notre pack ne remplit que les clés absentes.

## Builds Minecraft

| Cible | Version | Java | Langues | Contenu empaqueté |
|---|---|---:|---:|---|
| Minecraft 1.21.1 | `0.9.0-beta+1.21.1` | 21 | 85 | NeoOrigins + Medieval Origins Revival + ibarn's quartet origins addon + Origins Fantasy + Origins: Backgrounds + Origins: More Backgrounds + Origins: Backgrounds ISS + Origins Furries + Origins: Classes Extended + Origins: Classes ISS + Origin Architect |
| Minecraft 26.1 / 26.1.1 / 26.1.2 | `0.9.0-beta+26.1` | 25 | 85 | NeoOrigins uniquement + delta 26.1 |
| Minecraft 26.2 | `0.9.0-beta+26.2` | 25 | 85 | NeoOrigins uniquement + delta 26.2 |

Les builds 26.x n'embarquent aucune traduction des add-ons 1.21.1. La CI construit et audite séparément les trois cibles.

## Langues

La **0.9.0 Beta** prend en charge : Français (`fr_fr`), Allemand (`de_de`), Espagnol (`es_es`), Portugais brésilien (`pt_br`), Néerlandais (`nl_nl`), Italien (`it_it`), Polonais (`pl_pl`), Russe (`ru_ru`), Turc (`tr_tr`), Chinois simplifié (`zh_cn`), **Tchèque (`cs_cz`)**, **Hongrois (`hu_hu`)**, **Japonais (`ja_jp`)**, **Coréen (`ko_kr`)**, **Ukrainien (`uk_ua`)**, **Indonésien (`id_id`)**, **Suédois (`sv_se`)**, **Danois (`da_dk`)**, **Finnois (`fi_fi`)**, **Norvégien bokmål (`no_no`)**, **Roumain (`ro_ro`)**, **Grec (`el_gr`)**, **Bulgare (`bg_bg`)**, **Vietnamien (`vi_vn`)**, **Arabe (`ar_sa`)**, **Hébreu (`he_il`)**, **Thaï (`th_th`)**, **Slovaque (`sk_sk`)**, **Slovène (`sl_si`)**, **Croate (`hr_hr`)**, **Serbe cyrillique (`sr_sp`)**, **Serbe latin (`sr_cs`)**, **Catalan (`ca_es`)**, **Estonien (`et_ee`)**, **Lituanien (`lt_lt`)**, **Letton (`lv_lv`)**, **Basque (`eu_es`)**, **Galicien (`gl_es`)**, **Hindi (`hi_in`)**, **Norvégien nynorsk (`nn_no`)**, **Persan (`fa_ir`)**, **Islandais (`is_is`)**, **Malais (`ms_my`)**, **Filipino (`fil_ph`)**, **Gallois (`cy_gb`)**, **Irlandais (`ga_ie`)**, **Gaélique écossais (`gd_gb`)**, **Arménien (`hy_am`)**, **Géorgien (`ka_ge`)**, **Kazakh (`kk_kz`)**, **Mongol (`mn_mn`)**, **Macédonien (`mk_mk`)**, **Biélorusse (`be_by`)**, **Féroïen (`fo_fo`)**, **Afrikaans (`af_za`)**, **Azéri (`az_az`)**, **Kannada (`kn_in`)**, **Tchouvache (`cv_cu`)**, **Ouzbek (`uz_uz`)**, **Maltais (`mt_mt`)**, **Luxembourgeois (`lb_lu`)**, **Somali (`so_so`)**, **Espéranto (`eo_uy`)**, **Kirghize (`ky_kg`)**, **Tamoul (`ta_in`)**, **Albanais (`sq_al`)**, **Lao (`lo_la`)**, **Bosnien (`bs_ba`)**, **Bachkir (`ba_ru`)**, **Breton (`br_fr`)**, **Asturien (`ast_es`)**, **Frison occidental (`fy_nl`)**, **Occitan (`oc_fr`)**, **Igbo (`ig_ng`)**, **Yoruba (`yo_ng`)** et **Tatar (`tt_ru`)**, **Chinois traditionnel (`zh_tw`)** et **Same du Nord (`se_no`)** et **Bavarois (`bar`)** et **Brabançon (`brb`)** et **Andalou (`esan`)** et **Francique oriental (`fra_de`)** et **Frioulan (`fur_it`)** et **Gallo (`go_fr`)** et **Mannois (`gv_im`)**.

Les quatre-vingt-cinq langues sont disponibles sur les trois builds pour NeoOrigins. Les traductions d'add-ons sont empaquetées uniquement sur Minecraft 1.21.1 lorsqu'une version compatible de l'add-on est réellement disponible.

## Référence NeoOrigins

La référence d'audit actuelle est **NeoOrigins 2.2.27** :

- 1.21.1 : commit `af467a3bc118f6bbc0970d68f7e03fa631d7e6f2` ;
- 26.1.x : commit `aa207ef14cf3b938e28b4081162701953957c1d5` ;
- 26.2 : commit `511cadcafe3027d2a56b4448652ec9b74e2f3b07`.

Le fichier anglais `en_us.json` de NeoOrigins 2.2.27 est **strictement identique à celui de 2.2.26** sur les trois cibles : cette mise à jour n'ajoute donc aucune chaîne à traduire. La 2.2.27 est essentiellement un hotfix NeoForge.

L’audit intégral initial des 58 locales avait révélé sept lacunes historiques, antérieures à la 2.2.27. Elles ont depuis été récupérées avant la langue #59 : italien, polonais, russe, chinois simplifié, turc, tchèque et hongrois sont désormais complets contre la baseline 2.2.27. L’audit qui avait exposé ces lacunes est le run `34400432957`.

Le namespace physique `neoorigins_226` conserve son nom historique car il contient le delta introduit avec la 2.2.26 ; il n'est pas renommé lors du passage de la baseline d'audit à 2.2.27.

Pour le tchèque :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le hongrois :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le coréen :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l'ukrainien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l'indonésien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le suédois :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le danois :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le finnois :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le norvégien bokmål :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le roumain :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le grec :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le bulgare :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le vietnamien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l'arabe :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l'hébreu :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le thaï :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le slovaque :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le slovène :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le croate :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le serbe cyrillique :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le serbe latin :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le catalan :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l'estonien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le lituanien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le letton :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le basque :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le galicien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le hindi :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le norvégien nynorsk :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le persan :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l'islandais :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le malais :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le filipino :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le gallois :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l’irlandais :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le gaélique écossais :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l’arménien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le géorgien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le kazakh :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le mongol :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le macédonien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le biélorusse :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le féroïen :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l'afrikaans :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l'azéri :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le kannada :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le tchouvache :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l’ouzbek :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le maltais :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le luxembourgeois :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le somali :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l’espéranto :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le kirghize :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le tamoul :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l’albanais :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le lao :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le bosnien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le bachkir :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le breton :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l'asturien :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le frison occidental :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l'occitan :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l'igbo :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le yoruba :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le tatar :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le chinois traditionnel :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le same du Nord :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le bavarois :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le brabançon :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour l'andalou :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le francique oriental :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le frioulan :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le gallo :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Pour le mannois :

- **1.21.1 : 2 296/2 296 clés** couvertes ;
- **26.1.x : 2 307/2 307 clés** couvertes ;
- **26.2 : 2 307/2 307 clés** couvertes.

Sur 26.x, trois anciennes clés de récompense restent dans les fichiers de fallback mais n'existent plus en amont ; elles sont signalées comme obsolètes par l'audit et restent sans effet.

## Projets pris en charge sur Minecraft 1.21.1

| Projet | Version/référence | Couverture CS / HU / JA / KO / UK / ID / SV / DA / FI / NO / RO / EL / BG / VI / AR / HE / TH / SK / SL / HR / SR-CYR / SR-LAT / CA / ET / LT / LV / EU / GL / HI / NN / FA / IS / MS / FIL / CY / GA / GD / HY / KA / KK / MN / MK / BE / FO / AF / AZ / KN | Couverture effective par langue |
|---|---|---:|---:|
| Medieval Origins Revival | branche `1.21.1-fabric` | 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 · 401/401 | 401/401 |
| ibarn's quartet origins addon | 1.7.1 | 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 · 69/69 | 69/69 |
| Origins Fantasy for NeoOrigins | 1.1.3 | 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 · 240/240 | 240/240 |
| Origins: Backgrounds for NeoOrigins | 1.0.2 | 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 · 65/65 | 65/65 |
| Origins: More Backgrounds for NeoOrigins | 1.0.2 | 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 · 44/44 | 39 propres + 5 partagées = 44/44 |
| Origins: Backgrounds ISS for NeoOrigins | 1.0.1 | 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 · 79/79 | 77 propres + 2 partagées = 79/79 |
| Origins Furries for NeoOrigins | 1.0.0 | 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 · 117/117 | 117/117 |
| Origins: Classes Extended for NeoOrigins | 1.0.1 | 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 · 124/124 | 124/124 |
| Origins: Classes ISS for NeoOrigins | 1.0.1 | 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 · 99/99 | 99/99 |
| Origin Architect | 3.0.1 | 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 (officiel) · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 · 22/22 | 22/22 |

Les intégrations DraconicArcher sont réalisées avec son autorisation explicite pour redistribuer les **chaînes de localisation traduites**. Aucun code, texture, modèle ou autre asset de gameplay de ces add-ons n'est redistribué ; les mods originaux restent requis.

Origins: Backgrounds ISS et Origins: Classes ISS nécessitent également **Iron's Spells 'n Spellbooks**. Origin Architect est suivi sur le commit source `f58a6261292942d4123c46ff221fbdade138a329`.

## Fonctionnement

Le resource pack intégré est placé en priorité basse :

1. les traductions officielles du mod/add-on sont prioritaires ;
2. les resource packs normaux peuvent les modifier ;
3. NeoOrigins Localization sert de fallback pour les clés restantes.

Aucune traduction n'est générée à l'exécution dans Minecraft.

## Audits et maintenance

La CI vérifie :

- la validité des JSON et l'absence de clés dupliquées ;
- les clés manquantes par rapport aux sources/JAR amont épinglés ;
- les overlaps avec les traductions officielles ;
- les placeholders `%s`, `%1$s`, `%d`, etc. ;
- l'empaquetage par cible ;
- la compilation Java/NeoForge des trois builds.

Les scripts suivis incluent :

```bash
python scripts/validate.py
python scripts/audit_neoorigins_upstream.py --fail-on-overlap --fail-on-missing
python scripts/audit_medievalorigins_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_ibarnorigins_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_fantasy_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_backgrounds_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_more_backgrounds_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_backgrounds_iss_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_furries_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_classes_extended_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origins_classes_iss_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_origin_architect_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
```

Lorsqu'un projet amont ajoute une traduction officielle, les clés devenues inutiles doivent être retirées de notre fallback.

## Validation des JAR 0.9.0

L'inspection des JAR construits avec la référence NeoOrigins 2.2.26 a confirmé :

- **1.21.1** : 35 fichiers `cs_cz` et **33 fichiers `hu_hu`** empaquetés, couvrant NeoOrigins, Medieval Origins et tous les add-ons listés ;
- **26.1.x** : 21 fichiers `cs_cz` et **20 fichiers `hu_hu`**, uniquement les namespaces NeoOrigins communs + `neoorigins_226` + `neoorigins_26_1` ;
- **26.2** : 21 fichiers `cs_cz` et **20 fichiers `hu_hu`**, uniquement les namespaces NeoOrigins communs + `neoorigins_226` + `neoorigins_26_2` ;
- **suédois** : 27 fichiers `sv_se` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec les deltas de version corrects ;
- **danois** : 27 fichiers `da_dk` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec les deltas de version corrects ;
- **finnois** : 27 fichiers `fi_fi` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec les deltas de version corrects ;
- **norvégien bokmål** : 27 fichiers `no_no` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec les deltas de version corrects ;
- **roumain** : 26 fichiers fallback `ro_ro` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x ; Origin Architect fournit séparément ses 22/22 chaînes roumaines officielles ;
- **grec** : 27 fichiers `el_gr` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec les deltas de version corrects ;
- **bulgare** : 27 fichiers fallback `bg_bg` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **vietnamien** : 27 fichiers fallback `vi_vn` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **arabe** : 27 fichiers fallback `ar_sa` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **hébreu** : 27 fichiers fallback `he_il` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **thaï** : 27 fichiers fallback `th_th` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **slovaque** : 27 fichiers fallback `sk_sk` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **slovène** : 27 fichiers fallback `sl_si` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **croate** : 27 fichiers fallback `hr_hr` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **serbe cyrillique** : 27 fichiers fallback `sr_sp` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **serbe latin** : 27 fichiers fallback `sr_cs` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **catalan** : 27 fichiers fallback `ca_es` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **estonien** : 27 fichiers fallback `et_ee` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **lituanien** : 27 fichiers fallback `lt_lt` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **letton** : 27 fichiers fallback `lv_lv` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **basque** : 27 fichiers fallback `eu_es` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **galicien** : 27 fichiers fallback `gl_es` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **hindi** : 27 fichiers fallback `hi_in` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **norvégien nynorsk** : 27 fichiers fallback `nn_no` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **persan** : 27 fichiers fallback `fa_ir` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **islandais** : 27 fichiers fallback `is_is` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **malais** : 27 fichiers fallback `ms_my` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **filipino** : 27 fichiers fallback `fil_ph` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **gallois** : 27 fichiers fallback `cy_gb` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **irlandais** : 27 fichiers fallback `ga_ie` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **gaélique écossais** : 27 fichiers fallback `gd_gb` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **arménien** : 27 fichiers fallback `hy_am` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **géorgien** : 27 fichiers fallback `ka_ge` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **kazakh** : 27 fichiers fallback `kk_kz` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **mongol** : 27 fichiers fallback `mn_mn` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **macédonien** : 27 fichiers fallback `mk_mk` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **biélorusse** : 27 fichiers fallback `be_by` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **féroïen** : 27 fichiers fallback `fo_fo` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **afrikaans** : 27 fichiers fallback `af_za` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **azéri** : 27 fichiers fallback `az_az` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- **kannada** : 27 fichiers fallback `kn_in` dans le JAR 1.21.1 et 17 dans chacun des JAR 26.x, avec priorité conservée aux traductions officielles amont ;
- aucun namespace d'add-on 1.21.1 n'est présent dans les JAR 26.x ;
- les trois builds compilent avec succès et leur contenu de localisation a été ouvert et validé après construction.

La validation automatisée ne remplace pas un contrôle visuel en jeu pour la qualité de formulation ou les problèmes de largeur d'interface.

## Traduction et retours

Les traductions et leur maintenance utilisent une assistance générative/automatisée importante, avec contrôles de structure et direction humaine. Elles ne sont pas présentées comme des traductions intégralement relues par des locuteurs natifs. Les corrections de formulation et de terminologie sont bienvenues.

Un nom d'Origin est traduit seulement lorsque le résultat reste naturel, identifiable et lisible dans l'interface ; sinon le nom anglais peut être conservé.

## Licences et attributions

Le code et la documentation originaux de NeoOrigins Localization sont sous licence MIT. Les éléments dérivés de projets tiers restent soumis aux licences ou autorisations amont applicables. Voir [`docs/ATTRIBUTIONS.md`](docs/ATTRIBUTIONS.md).

Le fichier [`catalog.json`](catalog.json) est la source de vérité du contenu suivi ; [`CATALOG.md`](CATALOG.md) en est la vue lisible.
