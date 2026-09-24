# Portfolio — Jeremie Katolo

Portfolio professionnel dynamique, sécurisé et administrable.

## Positionnement

**Network & Cybersecurity Engineer**
**Ingénieur Réseaux & Cybersécurité**

Domaines :
- Réseaux
- Cybersécurité
- Systèmes
- Infrastructure
- Automatisation

## Principes du projet

Ce portfolio est conçu comme une **plateforme professionnelle dynamique**, et non comme un site statique.

- **Code ≠ Contenu** : le contenu est stocké en base de données et administrable après déploiement.
- **Proof-first** : chaque compétence affirmée doit pouvoir être reliée à une preuve (projet, lab, étude de cas).
- **Sécurité par défaut** : le portfolio applique lui-même les principes de sécurité qu’il présente.
- **Documentation** : architecture, UML, MERISE, ADR, threat model.
- **Évolutivité** : ajout de contenu en production sans modification du code source.

## Architecture cible (à construire)

```text
React (frontend)
     ↓ HTTPS / REST
Django + DRF (backend, API, admin)
     ↓
PostgreSQL (données)