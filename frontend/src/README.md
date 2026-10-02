# Structure de `frontend/src/`

## Organisation
src/
├── assets/ Images, logos, polices locales
├── components/ Composants réutilisables (Button, Card, Input, Badge...)
├── contexts/ React Contexts (ThemeContext...)
├── features/ Modules métier (projets/, articles/, auth/...)
├── hooks/ Hooks React custom (useTheme, useProjets...)
├── layouts/ Layouts (MainLayout, Header, Footer...)
├── pages/ Pages (HomePage, ProjetsPage, ProjetDetailPage...)
├── services/ Appels API (client.ts, projets.ts, articles.ts...)
├── types/ Types TypeScript (projet.ts, article.ts, api.ts...)
├── utils/ Helpers (formatDate, slugify, cn...)
├── App.tsx Composant racine
├── main.tsx Point d'entrée
└── index.css Tailwind + configuration globale

## Conventions

- **Composant** : un fichier par composant, `PascalCase.tsx` (ex. `Button.tsx`).
- **Hook** : un fichier par hook, `camelCase.ts` préfixé par `use` (ex. `useTheme.ts`).
- **Type** : un fichier par domaine, `camelCase.ts` (ex. `projet.ts`).
- **Service** : un fichier par ressource API, `camelCase.ts` (ex. `projets.ts`).
- **Page** : un composant par page, `PascalCasePage.tsx` (ex. `HomePage.tsx`).

## Alias TypeScript

Un alias `@/` est configuré pour pointer vers `src/`.
Exemple : `import { Button } from '@/components/Button'`