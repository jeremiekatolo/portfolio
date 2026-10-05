/**
 * Types correspondant à l'app `articles`.
 */

import type { Categorie } from './categories'
import type { CompetenceInline } from './competences'
import type { Statut } from './projets'
import type { TechnologieInline } from './technologies'
import type { MediaInline } from './utilisateurs'
import type { LienExterneInline } from './projets'


export interface Article {
  id: number
  titre: string
  slug: string
  resume: string
  contenu: string
  temps_lecture: number
  statut: Statut
  statut_display: string
  publish_at: string | null
  unpublish_at: string | null
  categorie: Categorie
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