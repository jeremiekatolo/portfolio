import { Link } from 'react-router-dom'
import { ArrowLeft, FlaskConical } from 'lucide-react'

import { Badge } from '@/components/ui/Badge'
import type { Laboratoire } from '@/types'

interface LabHeaderProps {
  lab: Laboratoire
}

export function LabHeader({ lab }: LabHeaderProps) {
  return (
    <div className="mb-10">
      <Link
        to="/labs"
        className="inline-flex items-center gap-1 text-sm text-slate-500 dark:text-slate-500 hover:text-sky-600 dark:hover:text-sky-400 transition-colors"
      >
        <ArrowLeft size={14} />
        Retour aux laboratoires
      </Link>

      <div className="mt-6 flex flex-wrap gap-2">
        <Badge variant="sky">
          <FlaskConical size={12} className="mr-1" />
          Laboratoire
        </Badge>
        <Badge>{lab.difficulte_display}</Badge>
        {lab.statut !== 'publie' && (
          <Badge variant="amber">{lab.statut_display}</Badge>
        )}
      </div>

      <h1 className="mt-6 text-4xl md:text-5xl font-bold text-slate-900 dark:text-slate-100">
        {lab.titre}
      </h1>

      {lab.objectif && (
        <p className="mt-4 text-xl text-slate-600 dark:text-slate-400 max-w-3xl">
          {lab.objectif}
        </p>
      )}
    </div>
  )
}