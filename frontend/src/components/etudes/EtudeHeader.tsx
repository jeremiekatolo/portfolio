import { Link } from 'react-router-dom'
import { ArrowLeft, Briefcase } from 'lucide-react'

import { Badge } from '@/components/ui/Badge'
import type { EtudeDeCas } from '@/types'

interface EtudeHeaderProps {
  etude: EtudeDeCas
}

export function EtudeHeader({ etude }: EtudeHeaderProps) {
  return (
    <div className="mb-10">
      <Link
        to="/etudes-de-cas"
        className="inline-flex items-center gap-1 text-sm text-slate-500 dark:text-slate-500 hover:text-sky-600 dark:hover:text-sky-400 transition-colors"
      >
        <ArrowLeft size={14} />
        Retour aux études de cas
      </Link>

      <div className="mt-6 flex flex-wrap gap-2">
        <Badge variant="sky">
          <Briefcase size={12} className="mr-1" />
          Étude de cas
        </Badge>
        {etude.statut !== 'publie' && (
          <Badge variant="amber">{etude.statut_display}</Badge>
        )}
      </div>

      <h1 className="mt-6 text-4xl md:text-5xl font-bold text-slate-900 dark:text-slate-100">
        {etude.titre}
      </h1>

      {etude.probleme && (
        <p className="mt-4 text-xl text-slate-600 dark:text-slate-400 max-w-3xl">
          {etude.probleme}
        </p>
      )}
    </div>
  )
}