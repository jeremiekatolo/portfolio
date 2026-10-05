import { Link } from 'react-router-dom'
import { ArrowLeft, Clock, FileText } from 'lucide-react'

import { Badge } from '@/components/ui/Badge'
import type { Article } from '@/types'

interface ArticleHeaderProps {
  article: Article
}

export function ArticleHeader({ article }: ArticleHeaderProps) {
  return (
    <div className="mb-10">
      <Link
        to="/articles"
        className="inline-flex items-center gap-1 text-sm text-slate-500 dark:text-slate-500 hover:text-sky-600 dark:hover:text-sky-400 transition-colors"
      >
        <ArrowLeft size={14} />
        Retour aux articles
      </Link>

      <div className="mt-6 flex flex-wrap gap-2">
        <Badge variant="sky">
          <FileText size={12} className="mr-1" />
          {article.categorie.nom}
        </Badge>
        {article.statut !== 'publie' && (
          <Badge variant="amber">{article.statut_display}</Badge>
        )}
      </div>

      <h1 className="mt-6 text-4xl md:text-5xl font-bold text-slate-900 dark:text-slate-100">
        {article.titre}
      </h1>

      {article.resume && (
        <p className="mt-4 text-xl text-slate-600 dark:text-slate-400 max-w-3xl">
          {article.resume}
        </p>
      )}

      <div className="mt-6 flex flex-wrap items-center gap-x-6 gap-y-2 text-sm text-slate-500 dark:text-slate-500">
        <span className="inline-flex items-center gap-1.5">
          <Clock size={14} />
          {article.temps_lecture} min de lecture
        </span>
        <span>Par {article.auteur_username}</span>
      </div>
    </div>
  )
}