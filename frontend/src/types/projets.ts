/**
 * Types correspondant à l'app `projets`.
 */

import type { Categorie } from './categories'
import type { CompetenceInline } from './competences'
import type { MediaInline } from './utilisateurs'
import type { TechnologieInline } from './technologies'

export type Statut = 'brouillon' | 'en_revision' | 'valide' | 'publie' | 'archive'
export type Difficulte = 'debutant' | 'intermediaire' | 'avance' | 'expert'

export type TypeLienExterne =
  | 'github'
  | 'demo'
  | 'documentation'
  | 'video'
  | 'article'
  | 'autre'

export interface LienExterneInline {
  id: number
  type: TypeLienExterne
  type_display: string
  url: string
  label: string
  ordre: number
}

export interface Projet {
  id: number
  titre: string
  slug: string
  resume: string
  description: string
  probleme: string
  contexte: string
  objectifs: string
  architecture_texte: string
  role: string
  difficulte: Difficulte
  difficulte_display: string
  statut: Statut
  statut_display: string
  publish_at: string | null
  unpublish_at: string | null
  date_realisation: string | null
  duree: string
  resultats: string
  limites: string
  ameliorations_futures: string
  categorie: Categorie
  laboratoire_titre: string | null
  etude_de_cas_titre: string | null
  technologies: TechnologieInline[]
  competences: CompetenceInline[]
  liens_externes: LienExterneInline[]
  mis_en_avant: boolean
  ordre: number
  seo_titre: string
  seo_description: string
  seo_image: MediaInline | null
  auteur_username: string
  date_creation: string
  date_modification: string
  est_public: boolean
}