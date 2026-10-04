/**
 * Types correspondant à l'app `laboratoires`.
 */

import type { CompetenceInline } from './competences'
import type { TechnologieInline } from './technologies'
import type { Difficulte, Statut } from './projets'
import type { MediaInline } from './utilisateurs'
import type { LienExterneInline } from './projets'

export interface Laboratoire {
  id: number
  titre: string
  slug: string
  objectif: string
  problematique: string
  environnement: string
  architecture_texte: string
  materiel_vm: string
  prerequis: string
  configuration: string
  tests: string
  resultats: string
  incidents_rencontres: string
  corrections: string
  analyse_securite: string
  limites: string
  ameliorations: string
  difficulte: Difficulte
  difficulte_display: string
  statut: Statut
  statut_display: string
  publish_at: string | null
  unpublish_at: string | null
  technologies: TechnologieInline[]
  competences: CompetenceInline[]
  ordre: number
  seo_titre: string
  seo_description: string
  seo_image: MediaInline | null
  auteur_username: string
  date_creation: string
  date_modification: string
  est_public: boolean
  liens_externes: LienExterneInline[]
}