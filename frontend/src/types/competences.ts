/**
 * Types correspondant à l'app `competences`.
 *
 * Règle métier : AUCUN champ de type pourcentage ou niveau.
 */

export type Domaine =
  | 'reseaux'
  | 'cybersecurite'
  | 'systemes'
  | 'automatisation'
  | 'developpement'

export interface Competence {
  id: number
  nom: string
  domaine: Domaine
  domaine_display: string
  description: string
  ordre: number
}

export interface CompetenceInline {
  id: number
  nom: string
  domaine: Domaine
}