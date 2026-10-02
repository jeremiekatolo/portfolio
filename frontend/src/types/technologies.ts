/**
 * Types correspondant à l'app `technologies`.
 */

export interface Technologie {
  id: number
  nom: string
  categorie_tech: string
  categorie_tech_display: string
  description: string
  url_officielle: string
  logo: { id: number; fichier: string; alt_text: string } | null
  ordre: number
}

export interface TechnologieInline {
  id: number
  nom: string
  categorie_tech: string
}