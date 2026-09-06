# NeoOrigins Localization

Mod client NeoForge fournissant des **traductions complémentaires** pour NeoOrigins et des packs/add-ons compatibles.

## Versions Minecraft

La bêta `0.6.0` est actuellement construite pour deux cibles :

- **Minecraft 1.21.1** — Java 21 — build `0.6.0-beta+1.21.1`
- **Minecraft 26.1.x** (`26.1`, `26.1.1`, `26.1.2`) — Java 25 — build `0.6.0-beta+26.1`

Le build 26.1.x compile contre **Minecraft 26.1.2 / NeoForge 26.1.2.29-beta** et déclare une plage Minecraft `[26.1,26.2)`, comme la branche 26.1.x de NeoOrigins. La compilation et l'audit de localisation sont validés ; la validation en jeu reste à effectuer avant de considérer cette cible comme stable.

Les add-ons tiers ne sont annoncés comme compatibles que sur les versions où leur intégration a été vérifiée. Medieval Origins Revival et la version NeoForge d'ibarn's quartet origins addon restent pour l'instant documentés comme supportés sur Minecraft 1.21.1 uniquement.

## Principe

Le projet ne doit pas écraser volontairement une traduction déjà fournie par le mod d'origine.

Les traductions sont chargées depuis un resource pack intégré placé en **priorité basse** :

1. le mod/add-on installé fournit sa traduction officielle ;
2. les resource packs normaux peuvent la modifier ;
3. notre pack sert de **fallback** pour les clés absentes.

Aucune traduction automatique n'est faite dans Minecraft. Chaque langue/add-on ajouté au projet doit être traduit, vérifié et maintenu avant publication.

## Langues NeoOrigins

La première base couvre cinq langues :

- Français (`fr_fr`)
- Allemand (`de_de`)
- Espagnol (`es_es`)
- Portugais brésilien (`pt_br`)
- Néerlandais (`nl_nl`)

NeoOrigins 2.2.25 fournit déjà `fr_fr`, `de_de`, `es_es` et `pt_br`. Pour ces quatre langues, notre fallback contient **uniquement les clés absentes de l'upstream**. À la date du contrôle, cela représente 52 clés par langue.

NeoOrigins 2.2.25 ne fournit pas de néerlandais. Notre traduction `nl_nl` couvre donc les **2 281 clés anglaises**. Pour faciliter la maintenance, elle est répartie dans plusieurs namespaces de ressources complémentaires, sans clés dupliquées. Elle reste marquée comme nécessitant des retours de locuteurs natifs même si la couverture technique est complète.

## Medieval Origins Revival

La branche `1.21.1-fabric` de Medieval Origins Revival ne fournit actuellement aucune traduction officielle pour nos cinq langues cibles. Notre fallback couvre donc l'intégralité des **401 clés anglaises** en :

- Français (`fr_fr`)
- Allemand (`de_de`)
- Espagnol (`es_es`)
- Portugais brésilien (`pt_br`)
- Néerlandais (`nl_nl`)

La compatibilité via `config/originpacks/` et la traduction d'un Origin importé ont déjà été validées en jeu sur Minecraft 1.21.1. Les fichiers complets restent ouverts aux retours de locuteurs natifs pour affiner la formulation et la terminologie.

## ibarn's quartet origins addon

La version **1.7.1 pour Minecraft 1.21.1** ne fournit actuellement que `en_us`. Notre fallback couvre donc ses **69 clés anglaises** dans les cinq langues cibles.

Contrairement à Medieval Origins Revival, cet add-on contient du **code Java**, des effets et des entités personnalisés. Sa version NeoForge 1.21.1 doit donc être installée comme un mod classique dans `mods/`, et non dans `config/originpacks/`.

Une branche 26.1 existe en amont pour ibarn, mais elle est actuellement destinée à Fabric et sa structure de localisation diffère de la version NeoForge 1.21.1. Elle n'est donc pas annoncée comme compatible avec notre build NeoForge 26.1.x tant qu'une intégration réelle n'a pas été validée.

## Nettoyage lors des mises à jour

Les scripts `scripts/audit_neoorigins_upstream.py`, `scripts/audit_medievalorigins_upstream.py` et `scripts/audit_ibarnorigins_upstream.py` comparent nos fichiers avec les versions officielles. Ils permettent notamment de repérer :

- les nouvelles clés anglaises à traduire ;
- les clés qu'un projet vient de traduire officiellement ;
- les entrées devenues inutiles dans notre fallback ;
- les éventuelles clés obsolètes ;
- les erreurs de placeholders comme `%s`, `%1$s` et `%d`.

Le CI exécute l'audit NeoOrigins sur chaque cible Minecraft. Les audits Medieval Origins Revival et ibarn restent associés au build 1.21.1 tant que ces add-ons ne sont pas validés sur 26.1.x.

## Add-ons actuellement suivis

| Mod / add-on | Auteur | Lien | État |
|---|---|---|---|
| NeoOrigins | CyberDay | [CurseForge](https://www.curseforge.com/minecraft/mc-mods/neoorigins) | 1.21.1 + 26.1.x bêta ; FR/DE/ES/PT-BR complétés en fallback, NL complet |
| Medieval Origins Revival | MuonR / muon-rw | [CurseForge](https://www.curseforge.com/minecraft/mc-mods/medieval-origins-revival) | 1.21.1 : FR/DE/ES/PT-BR/NL complets |
| ibarn's quartet origins addon | ibarnstormer | [CurseForge](https://www.curseforge.com/minecraft/mc-mods/ibarns-custom-origins-addon) | NeoForge 1.21.1 : FR/DE/ES/PT-BR/NL complets ; 26.1.x non annoncé |

Le fichier `catalog.json` reste la source de vérité de la liste des contenus traduits. Voir aussi [`CATALOG.md`](CATALOG.md).

## Politique sur les noms

Un nom d'Origin est traduit seulement si la traduction reste naturelle, identifiable et suffisamment courte pour l'interface. Sinon, le nom anglais est conservé. La largeur réelle dans l'interface prime sur le simple nombre de caractères.

Pour le néerlandais notamment, plusieurs noms canoniques restent en anglais afin de préserver la recherche, l'identification et la compatibilité visuelle. Les retours joueurs pourront justifier quelques traductions ciblées.

## Licences tierces

Seuls les projets dont la licence permet clairement la redistribution/adaptation sont intégrés sans autorisation préalable. Les attributions et licences applicables sont documentées dans [`docs/ATTRIBUTIONS.md`](docs/ATTRIBUTIONS.md).

## Ajouter un add-on

Voir [`docs/ADDING_ADDON.md`](docs/ADDING_ADDON.md).

## Vérification

```bash
python scripts/validate.py
python scripts/audit_neoorigins_upstream.py --fail-on-overlap
python scripts/audit_medievalorigins_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
python scripts/audit_ibarnorigins_upstream.py --fail-on-overlap --fail-on-missing --fail-on-placeholders
```

Le workflow GitHub Actions génère automatiquement les JAR 1.21.1 et 26.1.x avec leurs versions de Java, NeoForge et format de resource pack respectifs.

## État actuel

- Minecraft 1.21.1 : build et tests de localisation existants validés
- Minecraft 26.1.x : build `0.6.0-beta+26.1` compilé avec Java 25, test en jeu à faire
- NeoForge
- architecture multilingue, multi-namespace et désormais multi-version
- base NeoOrigins 2.2.25 en cinq langues complète techniquement sur les deux cibles auditées
- Medieval Origins Revival couvert dans les cinq langues cibles pour la branche 1.21.1-fabric
- ibarn's quartet origins addon 1.7.1 NeoForge couvert dans les cinq langues cibles pour Minecraft 1.21.1
- fallback NeoOrigins validé en jeu sur 1.21.1
- import `originpacks` et traduction des Origins importés validés avec Medieval Origins Revival sur 1.21.1
- audits des traductions officielles intégrés au CI
