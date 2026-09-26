# QA linguistique — NeoOrigins 2.2.28

## Provenance et couverture
Les nouvelles clés anglaises sont épinglées sur les trois commits amont mentionnés dans `catalog.json`.
Le manifeste `localization/neoorigins_228_source.json` sépare 228 nouvelles clés communes,
8 exclusives à Minecraft 1.21.1, 1 exclusive à 26.1.x et 2 descriptions actualisées.
Tous les 92 fichiers de langue communs, 1.21.1 et 26.1.x ont passé l'audit structurel.
La version 26.2 n'exige aucun fichier delta supplémentaire.

## Statut éditorial
La génération s'appuie sur les traductions de référence déjà présentes, complétées par
traduction automatique ; elle ne constitue **pas une relecture par un locuteur natif**.
20 libellés français prioritaires ont été corrigés manuellement et la variante serbe
latine a été dérivée du cyrillique avec le translittérateur déjà utilisé dans ce dépôt.

**Variantes nécessitant une relecture prioritaire :** bas allemand (`nds_de`) et
Kölsch (`ksh`) — base allemande ; brabançon (`brb`) et limbourgeois (`li_li`) —
base néerlandaise ; bavarois (`bar`) et francique oriental (`fra_de`) —
base allemande ; andalou (`esan`) — base espagnole ; gallo (`go_fr`) —
base française ; asturien (`ast_es`) — repli espagnol ; interslave (`isv`) —
repli russe ; kabyle (`kab_kab`) — repli français ; ido (`io_en`) —
repli espéranto ; bachkir (`ba_ru`) — quelques chaînes de repli russes.
Ces équivalents garantissent temporairement l'affichage mais ne doivent pas être
décrits comme des traductions dialectales ou natives complètes.

## Tests manuels avant publication
Vérifier en jeu les libellés de configuration ajoutés (notamment les « ticks »),
les neuf entités nommées, « Claimed by %s » et les deux descriptions du Voleur.
Tester les caractères accentués, scripts non latins, textes longs et la priorité
des traductions officielles sur les fallbacks. Refaire le contrôle sur chacun
des trois JAR générés par CI. Les dictionnaires proxy nécessitent ensuite
une révision dédiée et des contributeurs compétents.
