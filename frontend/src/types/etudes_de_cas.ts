/**
 * Types correspondant à l'app `etudes_de_cas`.
 */

import type { CompetenceInline } from './competences'
import type { Statut } from './projets'
import type { TechnologieInline } from './technologies'
import type { MediaInline } from './utilisateurs'

export interface EtudeDeCas {
  id: number
  titre: string
  slug: string
  probleme: string
  contexte: string
  analyse: string
  exigences: string
  menaces: string
  architecture_texte: string
  choix_techniques: string
  implementation: string
  securisation: string
  tests: string
  resultats: string
  limites: string
  recommandations: string
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
}