> **EXERCICE PÉDAGOGIQUE ASSISTÉ PAR IA — données fictives. Aucun audit qualifié, conformité certifiée ou décision réelle d'homologation.**

# Dossier GRC pédagogique — espace documentaire fictif

Version : 1.0.0 — créé le 2026-11-12.

Périmètre : Étude fictive d'un service interne de gestion de dossiers techniques synthétiques : consultation, modification contrôlée et disponibilité. Le dossier structure les cinq ateliers EBIOS RM et une instruction simulée d'homologation. Aucun système métier réel n'est audité.

Gravité × vraisemblance : convention locale d'exercice, non une prescription ISO ou EBIOS RM. Une cible n'est pas un résultat obtenu.

Convention locale de l'exercice : gravité et vraisemblance de 1 à 4 ; score = gravité × vraisemblance ; 1–3 faible, 4–7 modéré, 8–11 élevé, 12–16 critique. Ces choix ne sont pas une prescription ISO ou EBIOS RM. Les cibles sont des hypothèses, jamais des résultats obtenus.

## Limites

- Aucune organisation ou personne réelle ; aucune donnée personnelle, secret ou information classifiée.
- Aucune désignation OIV/SIIV, conformité légale ou certification ISO établie.
- Aucune prestation PASSI qualifiée, labellisation EBIOS RM ou homologation réelle.
- Aucune mesure technique déployée : les documents préparés ne prouvent pas la mise en œuvre ni l'efficacité des contrôles.
- Aucune attaque, connexion à une cible ou collecte réseau exécutée.
- Un fichier de preuve ou un test local ne démontre pas l'efficacité dans un SI réel.
- Aucun audit PASSI, conformité ISO/LPM ou décision réelle d'homologation n'est prononcé.

## Risques : initial, courant et cible

| Risque | Initial | Courant | Cible non acquise | Statut | Actions |
|---|---|---|---|---|---|
| R-01 — Divulgation de dossiers via un accès fournisseur | 4 × 3 = 12 (critique) | 4 × 3 = 12 (critique) | 4 × 1 = 4 (modéré) | open | ACT-01, ACT-02, ACT-03, ACT-06, ACT-07 |
| R-02 — Falsification des validations par abus de privilèges | 3 × 3 = 9 (élevé) | 3 × 3 = 9 (élevé) | 3 × 2 = 6 (modéré) | open | ACT-01, ACT-03, ACT-05, ACT-06, ACT-07 |
| R-03 — Interruption documentaire et absence de reprise démontrée | 4 × 3 = 12 (critique) | 4 × 3 = 12 (critique) | 4 × 2 = 8 (élevé) | open | ACT-03, ACT-04, ACT-06, ACT-07 |

### R-01 — justifications

- Initial : La gravité reprend ER-01 et la vraisemblance SO-01 ; score initial 12 selon la convention locale.
- Courant : Aucune action technique n'est mise en œuvre. La rédaction de procédures ne réduit pas le risque courant, qui reste égal à l'initial.
- Cible : Cible hypothétique après restrictions d'accès, revue et contrôles démontrés. La vraisemblance cible 1 devra être réévaluée à partir de preuves ; elle n'est pas obtenue.

### R-02 — justifications

- Initial : La gravité reprend ER-02 et la vraisemblance SO-02 ; score initial 9 selon la convention locale.
- Courant : Les principes de séparation sont rédigés seulement ; aucune restriction technique ni revue indépendante n'est prouvée. Le risque courant ne baisse pas.
- Cible : Objectif indicatif sous réserve de séparation des rôles, contrôles et revue effective. Il ne constitue ni résultat mesuré ni acceptation.

### R-03 — justifications

- Initial : La gravité reprend ER-03 et la vraisemblance SO-03 ; score initial 12 selon la convention locale.
- Courant : Le runbook n'est pas un test de sauvegarde ou de restauration. Aucune capacité de reprise technique n'est démontrée ; le courant reste égal à l'initial.
- Cible : Hypothèse de diminution de vraisemblance après contrôles de sauvegarde, restauration et réponse à incident effectivement vérifiés ; objectif non atteint.

## Actions de traitement

| Statut | Nombre |
|---|---:|
| planned | 2 |
| documented | 5 |
| implemented_in_lab | 0 |

| Action | Risques | Responsable fictif | Échéance | Statut | Preuves |
|---|---|---|---|---|---|
| ACT-01 — Documenter la gestion des comptes et les revues d'accès | R-01, R-02 | Responsable des identités fictif | 2026-12-04 | documented | EV-PROCEDURES |
| ACT-02 — Préparer le cadrage des accès fournisseur | R-01 | Responsable des prestataires fictif | 2026-12-08 | documented | EV-PROCEDURES |
| ACT-03 — Planifier la collecte et la revue technique des journaux | R-01, R-02, R-03 | Responsable exploitation fictif | 2026-12-11 | planned |  |
| ACT-04 — Rédiger les prérequis et le runbook de restauration | R-03 | Responsable sauvegarde fictif | 2026-12-15 | documented | EV-RUNBOOK |
| ACT-05 — Documenter la séparation des rôles et la double validation | R-02 | Responsable métier fictif | 2026-12-09 | documented | EV-PROCEDURES |
| ACT-06 — Préparer une sensibilisation aux accès et aux incidents | R-01, R-02, R-03 | Référent sensibilisation fictif | 2026-12-16 | documented | EV-AWARENESS |
| ACT-07 — Planifier la revue indépendante et l'instruction du dossier | R-01, R-02, R-03 | Pilote GRC fictif | 2026-12-18 | planned | EV-AUDIT, EV-HOMO |

## Mesures de base

| Mesure | Statut déclaré | Preuves |
|---|---|---|
| BC-01 — Procédure de gestion des comptes et des accès rédigée | documented | EV-PROCEDURES |
| BC-02 — Restriction technique des accès fournisseur à préparer | planned |  |
| BC-03 — Collecte et revue des journaux à concevoir | planned |  |
| BC-04 — Procédure de sauvegarde et restauration rédigée | documented | EV-RUNBOOK |
| BC-05 — Support de sensibilisation préparé | documented | EV-AWARENESS |
| BC-06 — Procédure de réaction à incident préparée | documented | EV-RUNBOOK |
| BC-07 — Cadre de revue des risques et d'instruction du dossier documenté | documented | EV-ATELIERS, EV-HOMO |

## Empreintes des preuves

| ID | Fichier relatif | Taille (octets) | SHA-256 |
|---|---|---:|---|
| EV-ATELIERS | docs/ateliers-ebios-rm.md | 7952 | a729a21479855c3737ba16c15e62c647d475a8b62db69e30961e2ebbb0daef09 |
| EV-AUDIT | docs/preparation-audit-passi.md | 4522 | 289850c451b98dadc1a96185ef5dc56b0265017093f33571c406726ed3003cec |
| EV-AWARENESS | docs/sensibilisation.md | 4579 | d344550596f799ebeed609c2635a226ba00c1fd1c7e01b79520fe2c61864754e |
| EV-CONTEXT | docs/cadre-reglementaire.md | 4821 | 25d83a8097a1a575be04ab213ca1e73d89b1601dab5c2d424c8df4de60427c3d |
| EV-HOMO | docs/dossier-homologation-simule.md | 3990 | ceb353ad8d6e74142b3f94272118973880bf8a76157096c9e040386880b80b08 |
| EV-PROCEDURES | docs/procedures-securite.md | 5641 | 268bf93a4c3b8629780fc6fe6dba8b9e89cfd6225931dd0409d100c2bcdd78d0 |
| EV-REVIEW | evidence/document-review.md | 1887 | f7f9b31a97bdb930597a11001fa6b3435cbab8ad517cf4b496d92c9883d26ef7 |
| EV-RUNBOOK | docs/runbook-incidents-restauration.md | 5292 | 42a67e9735e43b77eb0e6c77c59ce9a5f62efa03fb9f04a8561f899cadc1ec07 |
| EV-SOURCES | docs/sources-officielles.md | 2060 | cbe542764ef56a8bbab3c5faef8b4fe454da70201493c9321b828ca2a3b0426a |

Le rapport JSON conserve les registres et références du scénario. Les empreintes identifient les octets lus ; elles ne certifient ni le contenu ni une conformité.

