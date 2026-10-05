import { BookOpen, Code2, ExternalLink, FileText, Video } from 'lucide-react'
import type { ComponentType } from 'react'

import { Badge } from '@/components/ui/Badge'
import { Card } from '@/components/ui/Card'
import type { Article, TypeLienExterne } from '@/types'

interface ArticleSidebarProps {
  article: Article
}

const ICONES_LIEN: Record<TypeLienExterne, ComponentType<{ size?: number }>> = {
  github: Code2,
  demo: ExternalLink,
  documentation: BookOpen,
  video: Video,
  article: FileText,
  autre: ExternalLink,
}

export function ArticleSidebar({ article }: ArticleSidebarProps) {
  const aDesLiens = article.liens_externes.length > 0

  return (
    <aside className="space-y-4 lg:sticky lg:top-24">
      {aDesLiens && (
        <Card className="p-5">
          <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 uppercase tracking-wide">
            Ressources
          </h3>
          <ul className="mt-3 space-y-2">
            {article.liens_externes.map((lien) => {
              const Icone = ICONES_LIEN[lien.type] ?? ExternalLink
              return (
                <li key={lien.id}>
                  <a
                    href={lien.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="group flex items-center gap-2 text-sm text-slate-700 dark:text-slate-300 hover:text-sky-600 dark:hover:text-sky-400 transition-colors"
                  >
                    <Icone size={16} />
                    <span className="flex-1 group-hover:underline">
                      {lien.label || lien.type_display}
                    </span>
                    <ExternalLink size={12} className="text-slate-400 dark:text-slate-600" />
                  </a>
                </li>
              )
            })}
          </ul>
        </Card>
      )}

      {article.technologies.length > 0 && (
        <Card className="p-5">
          <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 uppercase tracking-wide">
            Technologies
          </h3>
          <div className="mt-3 flex flex-wrap gap-1.5">
            {article.technologies.map((tech) => (
              <span
                key={tech.id}
                className="text-xs px-2 py-1 rounded bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300"
              >
                {tech.nom}
              </span>
            ))}
          </div>
        </Card>
      )}

      {article.competences.length > 0 && (
        <Card className="p-5">
          <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 uppercase tracking-wide">
            Compétences
          </h3>
          <div className="mt-3 flex flex-wrap gap-1.5">
            {article.competences.map((comp) => (
              <Badge key={comp.id} variant="sky">
                {comp.nom}
              </Badge>
            ))}
          </div>
        </Card>
      )}
    </aside>
  )
}