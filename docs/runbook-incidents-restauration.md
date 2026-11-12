# Runbook préparé — incident et restauration documentaire

Version 1.0 — 12 novembre 2026 — EV-RUNBOOK — ACT-04, BC-04 et BC-06.

Support de préparation sur données fictives, sans exécution d'incident, confinement, sauvegarde ou restauration. Il contribue à R-03 et définit une réponse documentaire également utile à R-01 et R-02. L'organisation opérationnelle, les délais de service et les outils restent à choisir avant toute application réelle.

## Conditions préalables

Le responsable exploitation devrait disposer d'un inventaire validé, d'une liste de contacts autorisés tenue hors du SI concerné, d'une procédure de décision, d'une sauvegarde accessible avec des privilèges séparés et d'un environnement de restauration isolé. Un responsable métier devrait fixer des objectifs de reprise et de perte de données ; aucun RTO ou RPO tenu n'est revendiqué ici.

Les interventions ne seraient conduites que sur un environnement autorisé, par les personnes habilitées. Ce runbook ne contient ni commande offensive ni secret, et ne demande aucune action sur un système tiers.

## 1. Réception et qualification du signalement

Consigner un identifiant d'incident, l'heure et le fuseau, la ressource concernée, le symptôme, la première observation et les actions déjà faites. Collecter uniquement les informations nécessaires ; éviter les mots de passe, données personnelles et copies inutiles.

Déterminer si le signalement concerne la disponibilité (BV-03), une divulgation possible (BV-01), l'intégrité des validations (BV-02) ou plusieurs dimensions. Un arrêt de service ne prouve pas un rançongiciel, et une anomalie de connexion ne prouve pas une exfiltration. Les hypothèses seraient séparées des faits observés.

## 2. Escalade et préservation

Le coordinateur ferait confirmer le périmètre et les décisions urgentes par le responsable autorisé. Les journaux disponibles, versions et constats utiles seraient préservés de manière traçable, avec origine, heure, opérateur et empreinte si pertinent. La copie et l'accès aux éléments seraient restreints.

En cas de suspicion d'accès fournisseur non autorisé, une suspension ciblée de l'accès AS-06 serait soumise au responsable, en tenant compte de l'effet sur le service. En cas d'intégrité suspecte, les validations contestées seraient identifiées et soumises à une revue métier. Aucune suspension ou conservation réelle n'a été effectuée dans cet exercice.

## 3. Décision de reprise

Avant toute restauration, vérifier la cause probable, le périmètre de compromission, l'absence de dépendance toujours exposée et la provenance du point de reprise. Choisir un point antérieur à l'événement suspect selon les données disponibles, et obtenir une autorisation métier sur les éventuelles pertes de données.

Si la fiabilité du point de reprise ou de l'environnement cible est inconnue, maintenir la décision en attente et escalader ; ne pas déclarer un retour à un état sûr sans élément vérifiable.

## 4. Séquence de restauration proposée

1. Préparer une cible isolée et autorisée, séparée du service suspect.
2. Vérifier la présence, la lisibilité et l'intégrité de la sauvegarde choisie, ainsi que les dépendances applicatives nécessaires.
3. Restaurer le stockage AS-03 et les composants requis dans cette cible, conformément à des instructions techniques encore à rédiger pour la solution choisie.
4. Contrôler la cohérence des versions, un échantillon de dossiers synthétiques, les états de validation et les permissions.
5. Réaliser des tests autorisés d'accès attendu et refusé, puis un contrôle fonctionnel métier.
6. Mesurer l'heure de début, de fin et la perte de données réellement constatée lors du test.
7. Obtenir une décision explicite avant tout retour en service ; prévoir un repli si les critères ne sont pas tenus.

Cette liste est un plan de test, pas un procès-verbal de test. Aucun produit de sauvegarde n'a été installé et aucun temps de reprise n'a été mesuré.

## 5. Critères de succès à définir et à vérifier

| Critère | Preuve attendue | État du dossier |
| --- | --- | --- |
| Sauvegarde lisible et cohérente | Journal du test et vérification d'intégrité | Non disponible |
| Service fonctionnel dans la cible | Résultats de recette sur données synthétiques | Non disponible |
| Droits et validations corrects | Tests positifs/négatifs et revue métier | Non disponible |
| Délais de reprise acceptables | Mesures comparées aux objectifs approuvés | Objectifs et mesures absents |
| Cause et exposition maîtrisées | Analyse et validation de la correction | Non disponible |

## 6. Clôture et apprentissage

Un bilan distinguerait faits, hypothèses confirmées ou rejetées, cause, mesures prises, difficultés et actions restantes. Il mettrait à jour R-03 et, selon le cas, R-01/R-02. La réévaluation attendrait des preuves de contrôles réellement appliqués.

Pour ce dépôt, seule la rédaction du runbook est acquise. ACT-04 reste documentée et les scores courants ne baissent pas. La collecte des journaux ACT-03 est planifiée ; la préparation présente ne prouve pas qu'un système de détection ou d'alerte fonctionne.

