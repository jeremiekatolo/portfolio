import { Link } from 'react-router-dom'
import { ArrowRight, Calendar } from 'lucide-react'

import { Badge } from '@/components/ui/Badge'
import { Card } from '@/components/ui/Card'
import type { Projet } from '@/types'

interface ProjetCardProps {
  projet: Projet
}

export function ProjetCard({ projet }: ProjetCardProps) {
  return (
    <Card className="p-6 flex flex-col h-full">
      <div className="flex flex-wrap gap-2">
        <Badge variant="sky">{projet.categorie.nom}</Badge>
        <Badge>{projet.difficulte_display}</Badge>
        {projet.mis_en_avant && <Badge variant="amber">Mis en avant</Badge>}
      </div>

      <h3 className="mt-4 text-lg font-semibold text-slate-900 dark:text-slate-100 line-clamp-2">
        {projet.titre}
      </h3>

      <p className="mt-2 text-sm text-slate-600 dark:text-slate-400 line-clamp-3 flex-1">
        {projet.resume || projet.description.slice(0, 150)}
      </p>

      <div className="mt-4 flex flex-wrap gap-1.5">
        {projet.technologies.slice(0, 4).map((tech) => (
          <span
            key={tech.id}
            className="text-xs px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400"
          >
            {tech.nom}
          </span>
        ))}
        {projet.technologies.length > 4 && (
          <span className="text-xs px-2 py-0.5 text-slate-400 dark:text-slate-500">
            +{projet.technologies.length - 4}
          </span>
        )}
      </div>

      <div className="mt-4 pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
        {projet.date_realisation && (
          <span className="inline-flex items-center gap-1 text-xs text-slate-400 dark:text-slate-500">
            <Calendar size={12} />
            {new Date(projet.date_realisation).toLocaleDateString('fr-FR', {
              year: 'numeric',
              month: 'short',
            })}
          </span>
        )}
        <Link
          to={`/projets/${projet.slug}`}
          className="ml-auto inline-flex items-center gap-1 text-sm font-medium text-sky-600 dark:text-sky-400 hover:underline"
        >
          Découvrir
          <ArrowRight size={14} />
        </Link>
      </div>
    </Card>
  )
}