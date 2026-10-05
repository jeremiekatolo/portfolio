import { Link } from 'react-router-dom'
import { ArrowRight, Clock, FileText } from 'lucide-react'

import { Badge } from '@/components/ui/Badge'
import { Card } from '@/components/ui/Card'
import type { Article } from '@/types'

interface ArticleCardProps {
  article: Article
}

export function ArticleCard({ article }: ArticleCardProps) {
  return (
    <Card className="p-6 flex flex-col h-full">
      <div className="flex flex-wrap gap-2">
        <Badge variant="sky">
          <FileText size={12} className="mr-1" />
          {article.categorie.nom}
        </Badge>
        {article.statut !== 'publie' && (
          <Badge variant="amber">{article.statut_display}</Badge>
        )}
      </div>

      <h3 className="mt-4 text-lg font-semibold text-slate-900 dark:text-slate-100 line-clamp-2">
        {article.titre}
      </h3>

      <p className="mt-2 text-sm text-slate-600 dark:text-slate-400 line-clamp-3 flex-1">
        {article.resume}
      </p>

      {article.technologies.length > 0 && (
        <div className="mt-4 flex flex-wrap gap-1.5">
          {article.technologies.slice(0, 3).map((tech) => (
            <span
              key={tech.id}
              className="text-xs px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400"
            >
              {tech.nom}
            </span>
          ))}
          {article.technologies.length > 3 && (
            <span className="text-xs px-2 py-0.5 text-slate-400 dark:text-slate-500">
              +{article.technologies.length - 3}
            </span>
          )}
        </div>
      )}

      <div className="mt-4 pt-4 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
        <span className="inline-flex items-center gap-1 text-xs text-slate-400 dark:text-slate-500">
          <Clock size={12} />
          {article.temps_lecture} min
        </span>
        <Link
          to={`/articles/${article.slug}`}
          className="inline-flex items-center gap-1 text-sm font-medium text-sky-600 dark:text-sky-400 hover:underline"
        >
          Lire
          <ArrowRight size={14} />
        </Link>
      </div>
    </Card>
  )
}