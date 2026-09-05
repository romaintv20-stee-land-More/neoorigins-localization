# Ajouter un add-on

1. Vérifier le mod/add-on et identifier son `modid` / namespace.
2. Récupérer son fichier `en_us.json`.
3. Vérifier les fichiers de langues déjà présents.
4. Traduire et relire manuellement les chaînes à prendre en charge.
5. Ajouter le fichier dans :
   `src/main/resources/resourcepacks/fallback_localizations/assets/<namespace>/lang/<locale>.json`
6. Ajouter le projet et ses liens dans `catalog.json`.
7. Lancer `python scripts/validate.py`.
8. Tester en jeu avec le mod d'origine installé.

Ne jamais ajouter automatiquement un nouvel add-on détecté chez le joueur.
