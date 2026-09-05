# NeoOrigins Localization

Mod client NeoForge 1.21.1 fournissant des **traductions complémentaires** pour NeoOrigins et des packs/add-ons compatibles.

## Principe

Le projet ne doit pas écraser volontairement une traduction déjà fournie par le mod d'origine.

Les traductions sont chargées depuis un resource pack intégré placé en **priorité basse** :

1. le mod/add-on installé fournit sa traduction officielle ;
2. les resource packs normaux peuvent la modifier ;
3. notre pack sert de **fallback** pour les clés absentes.

Aucune traduction automatique n'est faite dans Minecraft. Chaque langue/add-on ajouté au projet doit être traduit et relu avant publication.

## Langues et mods actuellement pris en charge

| Mod / add-on | Auteur | Lien | État |
|---|---|---|---|
| NeoOrigins | CyberDay | [CurseForge](https://www.curseforge.com/minecraft/mc-mods/neoorigins) | Français + test néerlandais |
| Medieval Origins Revival | MuonR / muon-rw | [CurseForge](https://www.curseforge.com/minecraft/mc-mods/medieval-origins-revival) | Français, test partiel |

Pour Medieval Origins Revival, le premier test français couvre **Nain, Gorgone et Sirène** avec plusieurs de leurs pouvoirs. Le pack 1.21.1 peut être placé dans `originpacks/` de NeoOrigins ; la compatibilité réelle des pouvoirs doit être vérifiée en jeu avant de traduire tout le fichier.

Le fichier `catalog.json` est la source de vérité de cette liste. Voir aussi [`CATALOG.md`](CATALOG.md).

## Politique sur les noms

Un nom d'Origin est traduit seulement si la version française reste naturelle, identifiable et suffisamment courte pour l'interface. Sinon, le nom anglais est conservé.

## Licences tierces

Seuls les projets dont la licence permet clairement la redistribution/adaptation sont intégrés sans autorisation préalable. Les attributions et licences applicables sont documentées dans [`docs/ATTRIBUTIONS.md`](docs/ATTRIBUTIONS.md).

## Ajouter un add-on

Voir [`docs/ADDING_ADDON.md`](docs/ADDING_ADDON.md).

## Vérification

```bash
python scripts/validate.py
```

## État actuel

- Minecraft 1.21.1
- NeoForge
- architecture multilingue et multi-namespace
- NeoOrigins validé en jeu pour le fallback
- Medieval Origins Revival ajouté en test partiel
