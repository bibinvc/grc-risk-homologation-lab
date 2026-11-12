# Contrat de données — version 1

Projet pédagogique assisté par IA, créé le 12 novembre 2026. Toutes les organisations, personnes et situations sont fictives. Aucun audit qualifié, conformité certifiée ou décision réelle d'homologation.

Le fichier `data/scenario.json` est un objet contenant :

- `metadata`: `name`, `version`, `created` (ISO date), `educational` (true), `fictional` (true), `scoring_note` (texte), `scope`, `exclusions` (liste de textes).
- `business_values`: objets `id`, `name`, `mission`.
- `supporting_assets`: objets `id`, `name`, `business_value_ids` (références).
- `feared_events`: objets `id`, `name`, `business_value_id`, `severity` (entier 1–4), `rationale`.
- `baseline_controls`: objets `id`, `name`, `status` (`planned`, `documented` ou `implemented_in_lab`), `evidence_ids` (références). Une procédure rédigée ne prouve pas un contrôle déployé.
- `risk_sources`: objets `id`, `name`, `motivation`.
- `targeted_objectives`: objets `id`, `name`.
- `source_objective_pairs`: objets `id`, `risk_source_id`, `targeted_objective_id`, `retained` (booléen), `rationale`.
- `stakeholders`: objets `id`, `name`, `exposure`.
- `strategic_scenarios`: objets `id`, `name`, `pair_id` (paire retenue), `stakeholder_ids`, `feared_event_id`, `path` (liste de textes de haut niveau).
- `operational_scenarios`: objets `id`, `name`, `strategic_scenario_id`, `asset_ids`, `steps` (liste non offensive), `likelihood` (entier 1–4), `rationale`.
- `risks`: objets `id`, `name`, `operational_scenario_id`, `initial_severity`, `initial_likelihood`, `current_severity`, `current_likelihood`, `target_severity`, `target_likelihood` (entiers 1–4), `rationale`, `current_rationale`, `target_rationale`, `action_ids`, `status` (`open`, `treated`, `accepted_simulated`), `acceptance` (`null` ou objet `reviewer`, `date`, `rationale`, `simulated` true). L'initial correspond à la gravité de l'événement redouté et la vraisemblance du scénario opérationnel. Les mesures seulement planifiées/documentées ne réduisent jamais le risque courant. Une baisse du courant exige au moins une action `implemented_in_lab` avec des preuves, et une explication. Une cible n'est pas un résultat obtenu. L'acceptation simulée exige toutes les actions mises en œuvre dans le laboratoire et un dossier d'acceptation explicite.
- `treatment_actions`: objets `id`, `name`, `risk_ids`, `owner`, `due_date`, `status` (`planned`, `documented`, `implemented_in_lab`), `evidence_ids`. Les liens risque/action sont réciproques. Une action exécutée au laboratoire doit avoir une preuve existante ; ceci ne prouve pas son efficacité dans un SI réel.
- `evidence`: objets `id`, `path` relatif au dépôt, `description`. Les chemins doivent rester dans le dépôt, cibler des fichiers existants et être uniques. Le rapport recalcule SHA-256 et taille. Pas de preuve externe, secret ou pièce personnelle.

Toutes les listes sont obligatoires et non vides. Les identifiants sont uniques dans tout le jeu de données. Tous les textes requis sont non vides ; les dates sont des dates ISO valides. `evidence_ids` peut être vide sauf pour une mise en œuvre annoncée ; `acceptance` est null pour les risques ouverts. Les notes distinguent les cinq ateliers EBIOS RM, l'étude documentaire ISO 27001/27005, le contexte PASSI/LPM et l'instruction fictive d'homologation.

CLI Python standard sans dépendance : `python app.py validate [--data data/scenario.json]` et `python app.py report [--data ...] [--output reports]`. Les chemins sont résolus depuis la racine du projet, non le dossier courant. Validation invalide : code de sortie non nul, erreurs lisibles, aucun export de rapport. Rapport Markdown et JSON UTF-8 déterministe, risques initial/courant/cible séparés, compte des actions par statut, empreintes des preuves et avertissement pédagogique en tête. Pas d'exécution réseau ni de déploiement de sécurité par l'outil.

Les scores gravité × vraisemblance et niveaux (1–3 faible, 4–7 modéré, 8–11 élevé, 12–16 critique) sont une convention locale d'exercice, non une prescription ISO/EBIOS RM. Les tests doivent notamment vérifier les références brisées, doublons, échelles et types (booléen refusé en entier), dates, chemins hors dépôt/symlink, faux abaissement de risque, acceptation abusive, absence de preuve et séparation cible/courant.

