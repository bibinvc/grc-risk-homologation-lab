# Dossier pédagogique d'instruction d'homologation simulée

Version 1.0 — 12 novembre 2026 — EV-HOMO — contribution documentaire à ACT-07.

Ce dossier concerne un service documentaire entièrement fictif. Il prépare les questions qu'une autorité compétente pourrait examiner, mais il ne constitue pas une homologation. Aucune autorité réelle n'est désignée, aucun avis indépendant n'est disponible et aucune décision n'est signée.

## Objet et périmètre proposé

Le périmètre comprend l'application documentaire AS-01, l'annuaire AS-02, le stockage AS-03, la sauvegarde envisagée AS-04, la console d'administration AS-05 et l'accès fournisseur envisagé AS-06. Les missions sont la consultation, la modification contrôlée et la disponibilité de dossiers synthétiques. Les personnes, données et architectures décrites sont des hypothèses de laboratoire.

Sont exclus : tout SI opérationnel, donnée personnelle, information classifiée, réseau externe, engagement fournisseur réel, qualification PASSI, désignation OIV/SIIV et conformité réglementaire. La durée d'une éventuelle décision n'est pas proposée tant que le périmètre et les preuves ne sont pas confirmés.

## État du risque

| Risque | Initial et courant | Cible hypothétique | État de l'instruction |
| --- | --- | --- | --- |
| R-01, accès fournisseur et divulgation | 4 × 3 = 12, critique | 4 × 1 = 4, modéré | Ouvert ; restrictions, journaux et revue non démontrés |
| R-02, abus de privilèges et falsification | 3 × 3 = 9, élevé | 3 × 2 = 6, modéré | Ouvert ; séparation des rôles non testée |
| R-03, interruption et reprise non démontrée | 4 × 3 = 12, critique | 4 × 2 = 8, élevé | Ouvert ; aucun essai de restauration exécuté |

Le risque courant reste identique à l'initial. Les supports rédigés pour ACT-01, ACT-02, ACT-04, ACT-05 et ACT-06 sont des documents ; ils ne prouvent pas le déploiement des contrôles. ACT-03 et ACT-07 restent planifiées. La cible sert seulement à formuler un objectif de revue.

## Pièces disponibles

- Compte rendu pédagogique des cinq ateliers et registre JSON versionné.
- Procédures préparées pour les comptes, accès fournisseur et validations.
- Runbook de gestion d'incident et de restauration, non exécuté.
- Support de sensibilisation, non dispensé.
- Plan de préparation d'une revue et étude du contexte ISO, PASSI et LPM.
- Rapport généré de cohérence, incluant les empreintes des fichiers.

Les empreintes montrent quels octets ont été lus par l'outil. Elles ne démontrent ni l'efficacité d'une mesure ni la conformité du système.

## Lacunes bloquantes

1. Confirmer le périmètre, les responsables, les utilisateurs, les dépendances et les critères métier avec des acteurs réels autorisés.
2. Définir une architecture et une configuration de référence ; produire l'inventaire des flux et privilèges.
3. Mettre en œuvre et tester les restrictions d'accès, la journalisation, la séparation des rôles et la reprise.
4. Recueillir des preuves datées, attribuées et revues ; corriger les écarts.
5. Faire réexaminer gravité, vraisemblance, cibles et conditions de suivi par des personnes compétentes.
6. Déterminer les textes réellement applicables et, si nécessaire, le recours à une prestation qualifiée.
7. Obtenir l'avis des parties prévues par la gouvernance et une décision formelle de l'autorité compétente.

## Proposition soumise à décision

Au 12 novembre 2026, la proposition est **de ne pas prononcer d'homologation simulée favorable**. Les risques critiques restent ouverts et les preuves de mise en œuvre manquent. Une nouvelle instruction pourrait être ouverte après traitement et revue des points bloquants.

La [proposition de décision](decision-simulee-non-signee.md) reste volontairement non signée. Cette conclusion appartient à l'exercice et n'emporte aucun effet sur un système, une organisation ou un contrat réel.


