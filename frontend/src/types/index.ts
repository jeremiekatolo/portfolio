/**
 * Barrel export des types.
 *
 * Permet d'importer :
 *   import type { Projet, Article } from '@/types'
 * au lieu de :
 *   import type { Projet } from '@/types/projets'
 *   import type { Article } from '@/types/articles'
 */

export * from './api'
export * from './utilisateurs'
export * from './categories'
export * from './technologies'
export * from './competences'
export * from './projets'
export * from './laboratoires'
export * from './etudes_de_cas'
export * from './articles'