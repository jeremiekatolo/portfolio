/**
 * Types correspondant à l'app `categories`.
 */

export type CategorieType = 'projet' | 'laboratoire' | 'article' | 'etude_de_cas'

export interface Categorie {
  id: number
  nom: string
  slug: string
  type: CategorieType
  type_display: string
  description: string
  ordre: number
}