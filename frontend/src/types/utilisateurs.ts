/**
 * Types correspondant aux serializers de l'app `utilisateurs`.
 */

export type Role = 'visiteur' | 'editeur' | 'administrateur'

export interface Utilisateur {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  role: Role
  role_display: string
  is_active: boolean
  is_staff: boolean
  date_joined: string
  last_login: string | null
}

export interface MediaInline {
  id: number
  fichier: string
  alt_text: string
  type: string
}

export interface Profil {
  id: number
  utilisateur: number
  utilisateur_username: string
  nom_public: string
  titre_principal: string
  titre_secondaire: string
  bio_courte: string
  bio_longue: string
  email_public: string
  telephone_public: string
  localisation: string
  photo: MediaInline | null
  cv: MediaInline | null
  disponible: boolean
  seo_titre_defaut: string
  seo_description_defaut: string
  seo_image_defaut: MediaInline | null
  date_creation: string
  date_modification: string
}

export interface Me extends Utilisateur {
  is_superuser: boolean
  profil: Profil | null
}