# Procédures de sécurité préparées

Version 1.0 — 12 novembre 2026 — EV-PROCEDURES — actions ACT-01, ACT-02 et ACT-05.

Ces procédures sont rédigées pour le service documentaire fictif. Leur état est `documented` : elles n'ont été ni approuvées par une autorité réelle, ni appliquées à des comptes ou équipements, ni testées dans un SI. Les rôles sont des fonctions fictives sans nom, courriel ou donnée personnelle.

## P-01 — Création, modification et retrait des accès

Objectif : réduire à terme l'exposition de BV-01 et BV-02 aux scénarios SO-01 et SO-02. ACT-01 contribue à R-01 et R-02, sans réduction actuelle de score.

1. Le demandeur décrirait le besoin métier, la ressource AS-01/AS-03 concernée, le rôle demandé, le responsable et une date de fin. Une demande incomplète resterait en attente.
2. Le responsable métier vérifierait la nécessité et les éventuels conflits de rôles. Le demandeur ne validerait pas seul son propre besoin.
3. Le responsable des identités appliquerait uniquement les droits autorisés dans AS-02. L'usage d'un compte nominatif, d'une authentification renforcée adaptée et d'un profil minimal serait à définir et à mettre en œuvre.
4. Une vérification autorisée confirmerait les accès permis et refusés, ainsi que l'identité et la date de l'opérateur. Aucun mot de passe ou secret ne serait joint à la preuve.
5. À la sortie ou au changement de fonction, les droits devenus inutiles seraient retirés et les moyens d'authentification révoqués selon un délai à fixer.
6. Une revue périodique proposée, trimestrielle dans l'exercice et plus fréquente pour les privilèges, rapprocherait les droits effectifs, les demandes et les fonctions. Le responsable arbitrerait les écarts et suivrait leur clôture.

### Dossier de preuve requis avant de revendiquer une mise en œuvre

Demande autorisée et minimisée ; matrice des rôles ; configuration expurgée ; résultat d'un test positif et d'un test de refus ; trace de retrait ; compte rendu de revue et suivi des écarts. Aucun de ces éléments techniques n'est produit par ce document.

## P-02 — Accès de maintenance fournisseur

Objectif : traiter la dépendance PP-01 / AS-06 de R-01 par ACT-02.

Avant tout accès, le responsable des prestataires vérifierait le périmètre contractuel, le besoin, la durée, la responsabilité de validation et les exigences de sécurité applicables. Un intervenant identifié disposerait d'un accès limité au seul équipement nécessaire ; un accès permanent ou partagé demanderait une justification spécifique.

Le mécanisme à choisir devrait permettre une activation sur demande, une durée limitée, une authentification adaptée et la journalisation des opérations. Un créneau, un périmètre et une procédure de suspension seraient définis avant intervention. Le responsable vérifierait ensuite la fermeture de l'accès et les opérations réalisées.

L'autorisation de maintenance ne vaudrait pas autorisation générale de consulter ou exporter des dossiers. Tout besoin de transfert ferait l'objet d'une demande distincte, avec destinataire et canal autorisés. Une anomalie suivrait le runbook d'incident.

### Vérifications encore à réaliser

- Choisir et configurer le point d'accès, les restrictions réseau et l'authentification.
- Définir les événements de journalisation utiles et leurs modalités de revue dans ACT-03.
- Tester l'expiration, la révocation, les refus d'accès hors périmètre et la visibilité des événements.
- Obtenir une revue technique indépendante adaptée au périmètre avant de réévaluer la vraisemblance de R-01.

Ce dossier ne contient ni contrat réel, ni compte fournisseur, ni tunnel réseau, ni capture de configuration.

## P-03 — Séparation des rôles et validation des dossiers

Objectif : préparer ACT-05 pour R-02 et préserver BV-02.

| Fonction fictive | Droit envisagé | Restriction à implémenter |
| --- | --- | --- |
| Contributeur | Préparer ou corriger un dossier | Ne valide pas seul sa propre modification. |
| Validateur métier | Accepter ou refuser une version | Dispose d'une identité distincte de celle de l'auteur de cette version. |
| Administrateur technique | Maintenir le service | Ne transforme pas ce rôle en validation métier implicite. |
| Relecteur | Examiner les traces et écarts | Ne modifie pas les éléments qu'il contrôle pendant la revue. |

Une modification de validation conserverait l'ancienne valeur, la nouvelle valeur, la version du dossier, l'identité de l'acteur, la date et le motif, selon des paramètres de conservation à définir. Les opérations exceptionnelles resteraient visibles, justifiées, limitées dans le temps et revues. Une correction ne supprimerait pas silencieusement l'historique.

### Critères de recette envisagés

Une auto-validation doit être refusée ; un validateur distinct doit pouvoir agir sur la version prévue ; un compte technique ne doit pas obtenir les droits métier par défaut ; les tentatives refusées et validations autorisées doivent être retraçables. Ces critères ne sont pas des tests exécutés.

## Suivi documentaire

Les propriétaires et échéances proposés figurent dans `data/scenario.json`. Une modification de rôle, de fournisseur ou d'architecture déclencherait une revue des procédures et des risques liés. Pour marquer une action technique `implemented_in_lab`, il faudrait d'abord produire une preuve réelle de laboratoire, expliciter ce qu'elle démontre et conserver les limites du test. Le simple présent document ne suffit pas.

