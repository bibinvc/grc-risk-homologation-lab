# Cinq ateliers EBIOS Risk Manager — étude de cas pédagogique

Version 1.0 — 12 novembre 2026 — preuve documentaire EV-ATELIERS.

Ce document est un travail pédagogique assisté par IA sur un système entièrement fictif. Les « ateliers » désignent ici les étapes d'une étude rédigée : aucune réunion, consultation d'expert, collecte de terrain ou intervention technique réelle n'est revendiquée. La source méthodologique publique est l'[ANSSI](https://cyber.gouv.fr/securisation/analyse-des-risques/methode-ebios-rm/) ; le jeu de données ne constitue ni un outil labellisé ni une validation officielle de son application.

## Atelier 1 — Cadrage et socle de sécurité

Le service étudié permet de consulter des dossiers techniques synthétiques, de modifier leur état de validation et de les retrouver pendant une activité de démonstration. Il n'existe pas de véritable organisation cliente. Le périmètre couvre une application documentaire (AS-01), son annuaire (AS-02), son stockage (AS-03), une sauvegarde envisagée (AS-04), une console d'administration fictive (AS-05) et un point de maintenance fournisseur envisagé (AS-06). Les frontières et relations sont des hypothèses de conception.

| Valeur métier | Événement redouté | Gravité retenue | Justification pédagogique |
| --- | --- | --- | --- |
| BV-01 Confidentialité des dossiers | ER-01 Divulgation non autorisée | 4 | La divulgation étendue compromettrait la confidentialité prévue dans l'exercice. Aucune fuite réelle n'a eu lieu. |
| BV-02 Intégrité des validations | ER-02 Modification abusive | 3 | Des validations falsifiées rendraient les décisions métier peu fiables dans le scénario. |
| BV-03 Disponibilité du service | ER-03 Indisponibilité prolongée | 4 | L'activité fictive dépendrait de l'accès aux dossiers et ne disposerait pas d'une reprise démontrée. |

Le socle distingue les documents disponibles des contrôles techniques. BC-01, BC-04, BC-05, BC-06 et BC-07 sont documentés. BC-02 et BC-03 sont planifiés. Aucun contrôle n'est déclaré `implemented_in_lab`. Une procédure rédigée n'établit ni l'existence d'une configuration ni son efficacité.

## Atelier 2 — Sources de risque

Trois couples source de risque / objectif visé sont conservés. Il s'agit de menaces intentionnelles cohérentes avec les scénarios de l'exercice.

| Couple | Source / motivation | Objectif visé | Pourquoi le retenir |
| --- | --- | --- | --- |
| PAIR-01 | SR-01, acteur cybercriminel fictif recherchant une divulgation | OV-01, obtenir et divulguer les dossiers | La relation de maintenance envisagée introduit une dépendance à examiner. |
| PAIR-02 | SR-02, acteur interne malveillant fictif | OV-02, falsifier les validations | Des privilèges supposés sans séparation démontrée peuvent affecter l'intégrité métier. |
| PAIR-03 | SR-03, groupe d'extorsion fictif | OV-03, rendre le service indisponible | Une interruption délibérée exploiterait la dépendance au stockage et à la reprise. |

Ces motivations et capacités sont des hypothèses explicites, pas un renseignement sur un groupe réel. Les incidents accidentels et les défaillances sont à considérer dans le socle et la continuité ; ils ne sont pas artificiellement présentés comme une quatrième source intentionnelle.

## Atelier 3 — Scénarios stratégiques

L'écosystème comporte un fournisseur de maintenance (PP-01), une équipe d'administration (PP-02) et une équipe exploitation/sauvegarde (PP-03), tous fictifs. Leur exposition décrit ce qui serait à vérifier avant une mise en service, sans prétendre qu'un accès a été créé.

| Scénario | Chemin de haut niveau | Conséquence |
| --- | --- | --- |
| SS-01 / PAIR-01 / PP-01 | Relation fournisseur → accès de maintenance supposé → accès trop large aux dossiers | ER-01 |
| SS-02 / PAIR-02 / PP-02 | Rôle privilégié supposé → modification de validation insuffisamment séparée → décision métier altérée | ER-02 |
| SS-03 / PAIR-03 / PP-03 | Action volontaire sur le service → stockage rendu indisponible → reprise non démontrée | ER-03 |

Le choix d'un fournisseur comme dépendance ne signifie pas qu'il est compromis. Les chemins servent à définir des questions et mesures de protection ; ils ne décrivent pas une attaque effectivement exécutée.

## Atelier 4 — Scénarios opérationnels

SO-01 détaille SS-01 sur AS-06, AS-02, AS-01 et AS-03 : un usage non autorisé de l'accès fournisseur est supposé, les droits seraient trop larges et les dossiers deviendraient accessibles. SO-02 détaille SS-02 sur AS-02, AS-05 et AS-03 : un rôle privilégié serait utilisé pour modifier une validation sans séparation technique démontrée. SO-03 détaille SS-03 sur AS-01, AS-03 et AS-04 : une interruption volontaire affecterait le service alors qu'aucune restauration n'a été prouvée.

Chaque scénario reçoit une vraisemblance initiale de 3 sur 4. Le choix traduit une hypothèse prudente compte tenu des inconnues et de l'absence de contrôle technique démontré, et non une fréquence observée. Aucune commande offensive, exploitation, donnée extraite ou rançongiciel n'est nécessaire à ce dossier.

## Atelier 5 — Traitement du risque

### Convention locale de cotation

La gravité et la vraisemblance sont cotées de 1 à 4. Pour l'exercice, 1 signifie faible impact ou réalisation difficile avec obstacles démontrés, 2 un impact limité ou plusieurs conditions nécessaires, 3 un impact important ou un chemin plausible insuffisamment maîtrisé, 4 un impact majeur ou un chemin très accessible dans les hypothèses retenues. La gravité et la vraisemblance demeurent deux appréciations distinctes ; ces repères sont locaux et ne sont pas une échelle normative.

Le score local est gravité × vraisemblance : 1–3 faible, 4–7 modéré, 8–11 élevé, 12–16 critique. Aucun seuil ne déclenche une acceptation automatique. Les valeurs cibles décrivent des objectifs à réexaminer après preuve de mise en œuvre et vérification d'efficacité.

| Risque et chaîne | Initial | Courant | Cible hypothétique | Actions liées |
| --- | --- | --- | --- | --- |
| R-01 : BV-01 → ER-01 → PAIR-01 → SS-01 → SO-01 | 4 × 3 = 12, critique | 4 × 3 = 12, critique | 4 × 1 = 4, modéré | ACT-01, ACT-02, ACT-03, ACT-06, ACT-07 |
| R-02 : BV-02 → ER-02 → PAIR-02 → SS-02 → SO-02 | 3 × 3 = 9, élevé | 3 × 3 = 9, élevé | 3 × 2 = 6, modéré | ACT-01, ACT-03, ACT-05, ACT-06, ACT-07 |
| R-03 : BV-03 → ER-03 → PAIR-03 → SS-03 → SO-03 | 4 × 3 = 12, critique | 4 × 3 = 12, critique | 4 × 2 = 8, élevé | ACT-03, ACT-04, ACT-06, ACT-07 |

ACT-01, ACT-02, ACT-04, ACT-05 et ACT-06 disposent de supports rédigés. ACT-03 et ACT-07 restent planifiées. Les échéances du registre sont des dates de suivi proposées pour le scénario, pas la preuve d'un engagement d'une personne réelle. Les trois risques restent ouverts, sans acceptation. Le score courant demeure identique à l'initial.

La cible R-01 suppose notamment des restrictions fournisseur et revues vérifiées ; R-02 une séparation des rôles et une validation indépendante ; R-03 une reprise effectivement démontrée. Même la cible R-03 conserve un niveau élevé. Une future revue devrait challenger la pertinence des valeurs et l'effet propre de chaque mesure au lieu de diminuer mécaniquement les scores.

## Livrables et suite de l'instruction

Les procédures, le runbook, la sensibilisation préparée et le plan de revue sont référencés dans le registre. Le [dossier d'homologation simulée](dossier-homologation-simule.md) reprend ces inconnues. La prochaine étape serait de faire approuver le périmètre, déployer dans un laboratoire autorisé, recueillir les preuves appropriées, puis faire réexaminer les risques. Aucune de ces étapes futures n'est déclarée accomplie ici.

