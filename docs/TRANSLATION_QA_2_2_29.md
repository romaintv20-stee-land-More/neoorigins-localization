# Audit de compatibilité — NeoOrigins 2.2.29

Date de l'audit : **1er octobre 2026**.

## Résultat

NeoOrigins 2.2.29 ne modifie **aucun fichier de langue** par rapport aux références NeoOrigins 2.2.28 utilisées par NeoOrigins Localization 1.1.1, sur les trois cibles prises en charge.

| Cible | Référence 2.2.29 auditée | Clés anglaises | Changement de localisation depuis 2.2.28 |
|---|---|---:|---:|
| Minecraft 1.21.1 | `9a96c9f1a66b2a920f22e083d0563702c70f27c9` | 2 532 | 0 |
| Minecraft 26.1.x | `71e314492848a6f887e91f959c857a29822041d2` | 2 536 | 0 |
| Minecraft 26.2 | `8060d65189739a75785d885a8d87f795679bfd30` | 2 535 | 0 |

Les comparaisons Git ont été faites depuis les références 2.2.28 déjà figées dans la 1.1.1 :

- 1.21.1 : `87860513d5947fa0407a4dd1868126c9489e56cd` → `9a96c9f1a66b2a920f22e083d0563702c70f27c9` ;
- 26.1.x : `4f11c58362a7b3c76d5475ed072b79f49ceb537d` → `71e314492848a6f887e91f959c857a29822041d2` ;
- 26.2 : `d2d7c0b6d5439e11e3ed3e981dcdd25642f0b417` → `8060d65189739a75785d885a8d87f795679bfd30`.

Dans les trois comparaisons, aucun fichier sous `assets/neoorigins/lang/` n'est modifié.

## Conséquence pour NeoOrigins Localization

La **1.1.1 reste complète pour NeoOrigins 2.2.29**. Les ressources ajoutées pour 2.2.28 restent valides telles quelles et les namespaces `neoorigins_226` / `neoorigins_228_*` conservent volontairement leurs noms historiques.

Il n'y a donc **aucune raison de publier une 1.1.2 uniquement pour NeoOrigins 2.2.29**. Une nouvelle version de NeoOrigins Localization ne sera nécessaire que si une future version de NeoOrigins ajoute, retire ou modifie des chaînes, ou si le projet apporte ses propres changements.

## CI

La CI 1.1.1 est repointée vers les trois références 2.2.29 ci-dessus afin que les audits `--fail-on-missing`, `--fail-on-overlap` et `--fail-on-placeholders` continuent de valider directement la version amont actuelle.
