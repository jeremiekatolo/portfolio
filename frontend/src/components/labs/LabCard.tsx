import { Link } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'

import { Badge } from '@/components/ui/Badge'
import { Card } from '@/components/ui/Card'
import type { Laboratoire } from '@/types'

interface LabCardProps {
  lab: Laboratoire
}

export function LabCard({ lab }: LabCardProps) {
  return (
    <Card className="p-6 flex flex-col h-full">
      <div className="flex flex-wrap gap-2">
        <Badge variant="sky">Laboratoire</Badge>
        <Badge>{lab.difficulte_display}</Badge>
      </div>

      <h3 className="mt-4 text-lg font-semibold text-slate-900 dark:text-slate-100 line-clamp-2">
        {lab.titre}
      </h3>

      <p className="mt-2 text-sm text-slate-600 dark:text-slate-400 line-clamp-3 flex-1">
        {lab.objectif || lab.problematique.slice(0, 150)}
      </p>

      {lab.technologies.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-1.5">
          {lab.technologies.slice(0, 4).map((tech) => (
            <span
              key={tech.id}
              className="text-xs px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400"
            >
              {tech.nom}
            </span>
          ))}
          {lab.technologies.length > 4 && (
            <span className="text-xs px-2 py-0.5 text-slate-400 dark:text-slate-500">
              +{lab.technologies.length - 4}
            </span>
          )}
        </div>
      )}

      <div className="mt-4 pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-end">
        <Link
          to={`/labs/${lab.slug}`}
          className="inline-flex items-center gap-1 text-sm font-medium text-sky-600 dark:text-sky-400 hover:underline"
        >
          Découvrir
          <ArrowRight size={14} />
        </Link>
      </div>
    </Card>
  )
}