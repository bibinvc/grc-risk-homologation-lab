# Préparation d'une revue documentaire et contexte PASSI

Version 1.0 — 12 novembre 2026 — EV-AUDIT — contribution préparatoire à ACT-07.

Il s'agit d'un plan de préparation, pas d'un audit réalisé. Aucun auditeur indépendant n'a été mandaté, aucun contrôle technique ou test d'intrusion n'a été exécuté. La revue de cohérence produite par l'auteur du dépôt n'est pas indépendante.

## Ce que signifie PASSI dans ce dossier

Le référentiel public ANSSI PASSI concerne la qualification de prestataires d'audit de la sécurité des systèmes d'information et de leurs prestations dans un périmètre défini. Les familles couvertes comprennent notamment l'architecture, la configuration, le code source, les tests d'intrusion et l'audit organisationnel et physique. La qualification n'est pas un certificat personnel obtenu en rédigeant ce projet.

Le [référentiel officiel v2.2](https://cyber.gouv.fr/sites/default/files/document/PASSI_Referentiel-exigences_v2.2.pdf) est étudié pour comprendre les responsabilités et exigences d'une prestation. Le dépôt ne revendique ni prestation qualifiée, ni statut PASSI, ni conformité à l'ensemble de ce référentiel. Le besoin éventuel d'un prestataire qualifié serait déterminé selon le contexte réel et les exigences applicables.

## Mandat de revue envisagé

Objet : examiner la traçabilité des trois risques, les hypothèses du périmètre et l'état réel des preuves avant toute réévaluation ou instruction d'homologation. Le responsable du scénario, le responsable métier et une personne distincte chargée de la revue devraient d'abord convenir du périmètre, des critères, du calendrier et de la confidentialité.

La revue documentaire pourrait vérifier la présence et la cohérence des éléments. Elle ne démontrerait pas à elle seule l'efficacité des mesures techniques, même si tous les fichiers sont lisibles.

| Question de revue | Document disponible | Élément encore absent |
| --- | --- | --- |
| Les valeurs, actifs et événements redoutés sont-ils reliés ? | Registre et cinq ateliers | Confirmation par des responsables métier réels, hors périmètre du laboratoire |
| Les droits sont-ils minimaux et les départs traités ? | Procédure P-01 / ACT-01 | Configuration effective, échantillon de demandes et tests autorisés |
| Les accès fournisseur sont-ils bornés et révoqués ? | Procédure P-02 / ACT-02 | Configuration, traces d'activation et preuve de retrait |
| Les journaux détectent-ils les écarts pertinents ? | Action ACT-03 seulement planifiée | Architecture de collecte, événements, revue et essais |
| Une version peut-elle être auto-validée ? | Procédure P-03 / ACT-05 | Résultats de recette de la séparation des rôles |
| Le service est-il restaurable ? | Runbook / ACT-04 | Test exécuté, cohérence des données et mesure de reprise |
| La sensibilisation a-t-elle été dispensée ? | Support / ACT-06 | Session tenue et retour d'évaluation |
| Une autorité a-t-elle instruit et accepté les risques ? | Dossier et proposition non signée | Autorité réelle compétente, revue et décision ; aucune ici |

## Plan de travail proposé

1. Valider un mandat et séparer auteur, exploitant et relecteur autant que possible.
2. Geler une version du registre et des pièces, en conserver les empreintes et l'origine.
3. Réconcilier chaque action avec les preuves disponibles, en distinguant document, configuration et test exécuté.
4. Demander les compléments manquants ; ne pas les remplacer par une affirmation de l'auteur.
5. Classer les observations selon des critères convenus et discuter les faits avant conclusion.
6. Rédiger un rapport indiquant le périmètre, les limites, les écarts et les actions suivies.

Un test technique futur nécessiterait des règles d'engagement et autorisations explicites. Le présent projet se limite à la préparation et n'autorise aucune intervention sur un SI.

## Sortie attendue et état actuel

Un rapport de revue indépendante et un suivi des écarts seraient nécessaires pour conclure ACT-07. Ces pièces n'existent pas encore. Les empreintes calculées par l'outil attestent seulement les octets des documents exportés au moment du rapport ; elles ne constituent pas une preuve de conformité ni d'efficacité des contrôles.

ACT-07 reste `planned`. Tous les risques restent `open` avec un risque courant identique au risque initial. Aucun avis favorable, certification ou acceptation n'est signé.

