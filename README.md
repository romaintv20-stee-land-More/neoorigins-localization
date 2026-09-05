# NeoOrigins Localization

Mod client NeoForge 1.21.1 fournissant des **traductions complémentaires** pour NeoOrigins et des packs/add-ons compatibles.

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

## Nettoyage lors des mises à jour

Le script `scripts/audit_neoorigins_upstream.py` compare les fichiers du projet à la version officielle de NeoOrigins. Il permet notamment de repérer :

- les nouvelles clés anglaises à traduire ;
- les clés que NeoOrigins vient de traduire officiellement ;
- les entrées devenues inutiles dans notre fallback ;
- les éventuelles clés obsolètes ;
- les doublons entre les fichiers néerlandais répartis dans plusieurs namespaces.

Le CI exécute cet audit à chaque build. L'objectif est de retirer de notre mod toute entrée devenue officielle afin de garder les fichiers légers et de laisser la priorité au projet d'origine.

## Add-ons actuellement suivis

| Mod / add-on | Auteur | Lien | État |
|---|---|---|---|
| NeoOrigins | CyberDay | [CurseForge](https://www.curseforge.com/minecraft/mc-mods/neoorigins) | FR/DE/ES/PT-BR complétés en fallback, NL complet |
| Medieval Origins Revival | MuonR / muon-rw | [CurseForge](https://www.curseforge.com/minecraft/mc-mods/medieval-origins-revival) | Français, test partiel validé en jeu |

Le fichier `catalog.json` est la source de vérité de cette liste. Voir aussi [`CATALOG.md`](CATALOG.md).

## Politique sur les noms

Un nom d'Origin est traduit seulement si la traduction reste naturelle, identifiable et suffisamment courte pour l'interface. Sinon, le nom anglais est conservé. La largeur réelle dans l'interface prime sur le simple nombre de caractères.

Pour le néerlandais, les noms canoniques d'Origins restent actuellement majoritairement en anglais afin de préserver la recherche, l'identification et la compatibilité visuelle. Les retours joueurs pourront justifier quelques traductions ciblées.

## Licences tierces

Seuls les projets dont la licence permet clairement la redistribution/adaptation sont intégrés sans autorisation préalable. Les attributions et licences applicables sont documentées dans [`docs/ATTRIBUTIONS.md`](docs/ATTRIBUTIONS.md).

## Ajouter un add-on

Voir [`docs/ADDING_ADDON.md`](docs/ADDING_ADDON.md).

## Vérification

```bash
python scripts/validate.py
python scripts/audit_neoorigins_upstream.py --fail-on-overlap
```

## État actuel

- Minecraft 1.21.1
- NeoForge
- architecture multilingue et multi-namespace
- base NeoOrigins en cinq langues complète pour la version 2.2.25
- fallback NeoOrigins validé en jeu
- import `originpacks` validé avec Medieval Origins Revival
- audit des traductions officielles intégré au CI
