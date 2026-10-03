import { Link } from 'react-router-dom'
import { ArrowLeft, Calendar, Clock, Star } from 'lucide-react'

import { Badge } from '@/components/ui/Badge'
import type { Projet } from '@/types'

interface ProjetHeaderProps {
  projet: Projet
}

export function ProjetHeader({ projet }: ProjetHeaderProps) {
  return (
    <div className="mb-10">
      {/* Fil d'Ariane */}
      <Link
        to="/projets"
        className="inline-flex items-center gap-1 text-sm text-slate-500 dark:text-slate-500 hover:text-sky-600 dark:hover:text-sky-400 transition-colors"
      >
        <ArrowLeft size={14} />
        Retour aux projets
      </Link>

      {/* Badges */}
      <div className="mt-6 flex flex-wrap gap-2">
        <Badge variant="sky">{projet.categorie.nom}</Badge>
        <Badge>{projet.difficulte_display}</Badge>
        {projet.mis_en_avant && (
          <Badge variant="amber">
            <Star size={12} className="mr-1" />
            Mis en avant
          </Badge>
        )}
        {projet.statut !== 'publie' && (
          <Badge variant="amber">{projet.statut_display}</Badge>
        )}
      </div>

      {/* Titre */}
      <h1 className="mt-6 text-4xl md:text-5xl font-bold text-slate-900 dark:text-slate-100">
        {projet.titre}
      </h1>

      {/* Résumé */}
      {projet.resume && (
        <p className="mt-4 text-xl text-slate-600 dark:text-slate-400 max-w-3xl">
          {projet.resume}
        </p>
      )}

      {/* Métadonnées */}
      <div className="mt-6 flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-slate-500 dark:text-slate-500">
        {projet.date_realisation && (
          <span className="inline-flex items-center gap-1.5">
            <Calendar size={14} />
            {new Date(projet.date_realisation).toLocaleDateString('fr-FR', {
              year: 'numeric',
              month: 'long',
            })}
          </span>
        )}
        {projet.duree && (
          <span className="inline-flex items-center gap-1.5">
            <Clock size={14} />
            {projet.duree}
          </span>
        )}
        <span>Rôle : {projet.role || 'Non précisé'}</span>
      </div>
    </div>
  )
}