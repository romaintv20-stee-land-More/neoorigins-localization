# Ajouter un add-on

1. Vérifier le mod/add-on et identifier son `modid` / namespace.
2. Vérifier sa licence avant tout travail de redistribution.
   - Inclure sans demander uniquement si la licence autorise clairement la redistribution et les œuvres dérivées des fichiers concernés.
   - Exclure pour le moment les projets `All Rights Reserved`, sans licence, ou avec une licence personnalisée ambiguë.
   - Pour les licences avec obligations (GPL/LGPL/AGPL/MPL/CC BY, etc.), respecter leurs conditions avant intégration.
   - Si les ressources/textes ont une licence différente du code, c'est la licence des ressources/textes qui compte pour les fichiers de langue.
3. Récupérer son fichier `en_us.json`.
4. Vérifier les fichiers de langues déjà présents.
5. Traduire et relire manuellement les chaînes à prendre en charge.
6. Ajouter le fichier dans :
   `src/main/resources/resourcepacks/fallback_localizations/assets/<namespace>/lang/<locale>.json`
7. Ajouter le projet, ses liens et son statut de licence dans `catalog.json`.
8. Lancer `python scripts/validate.py`.
9. Tester en jeu avec le mod d'origine installé.

Ne jamais ajouter automatiquement un nouvel add-on détecté chez le joueur.

## Politique actuelle

Pendant la première phase du projet, nous ne contactons pas les auteurs pour demander une autorisation spéciale. Nous traduisons uniquement les add-ons dont la licence permet déjà clairement l'intégration et la redistribution de la localisation dans notre mod.
