# NeoOrigins Localization

Mod client NeoForge 1.21.1 fournissant des **traductions complémentaires** pour NeoOrigins et, à terme, ses add-ons.

## Principe

Le projet ne doit pas écraser volontairement une traduction déjà fournie par le mod d'origine.

Les traductions sont chargées depuis un resource pack intégré placé en **priorité basse** :

1. le mod/add-on installé fournit sa traduction officielle ;
2. les resource packs normaux peuvent la modifier ;
3. notre pack sert de **fallback** pour les clés absentes.

Aucune traduction automatique n'est faite dans Minecraft. Chaque langue/add-on ajouté au projet doit être traduit et relu avant publication.

## Langues et mods actuellement pris en charge

| Mod / add-on | Auteur | Lien | Français |
|---|---|---|---|
| NeoOrigins | CyberDay | [CurseForge](https://www.curseforge.com/minecraft/mc-mods/neoorigins) | ✅ |

Le fichier `catalog.json` est la source de vérité de cette liste.  
Quand le projet contiendra beaucoup de langues/add-ons, la page GitHub pourra être utilisée comme catalogue public unique.

## Ajouter un add-on

Voir [`docs/ADDING_ADDON.md`](docs/ADDING_ADDON.md).

## Vérification

```bash
python scripts/validate.py
```

## État de la V1

- Minecraft 1.21.1
- NeoForge
- Français uniquement
- NeoOrigins uniquement
- architecture déjà prévue pour plusieurs namespaces et plusieurs langues
