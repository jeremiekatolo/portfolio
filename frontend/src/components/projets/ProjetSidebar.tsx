import { ExternalLink } from 'lucide-react'

import { Badge } from '@/components/ui/Badge'
import { Card } from '@/components/ui/Card'
import type { Projet } from '@/types'

interface ProjetSidebarProps {
  projet: Projet
}

export function ProjetSidebar({ projet }: ProjetSidebarProps) {
  return (
    <aside className="space-y-4 lg:sticky lg:top-24">
      {/* Image SEO */}
      {projet.seo_image && (
        <Card className="overflow-hidden">
          <img
            src={projet.seo_image.fichier}
            alt={projet.seo_image.alt_text || projet.titre}
            className="w-full h-auto"
          />
        </Card>
      )}

      {/* Technologies */}
      {projet.technologies.length > 0 && (
        <Card className="p-5">
          <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 uppercase tracking-wide">
            Technologies
          </h3>
          <div className="mt-3 flex flex-wrap gap-1.5">
            {projet.technologies.map((tech) => (
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

      {/* Compétences */}
      {projet.competences.length > 0 && (
        <Card className="p-5">
          <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 uppercase tracking-wide">
            Compétences
          </h3>
          <div className="mt-3 flex flex-wrap gap-1.5">
            {projet.competences.map((comp) => (
              <Badge key={comp.id} variant="sky">
                {comp.nom}
              </Badge>
            ))}
          </div>
        </Card>
      )}

      {/* Informations */}
      <Card className="p-5">
        <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 uppercase tracking-wide">
          Informations
        </h3>
        <dl className="mt-3 space-y-2 text-sm">
          <div className="flex justify-between gap-2">
            <dt className="text-slate-500 dark:text-slate-500">Catégorie</dt>
            <dd className="text-slate-900 dark:text-slate-100 text-right">
              {projet.categorie.nom}
            </dd>
          </div>
          <div className="flex justify-between gap-2">
            <dt className="text-slate-500 dark:text-slate-500">Difficulté</dt>
            <dd className="text-slate-900 dark:text-slate-100 text-right">
              {projet.difficulte_display}
            </dd>
          </div>
          <div className="flex justify-between gap-2">
            <dt className="text-slate-500 dark:text-slate-500">Auteur</dt>
            <dd className="text-slate-900 dark:text-slate-100 text-right">
              {projet.auteur_username}
            </dd>
          </div>
        </dl>
      </Card>

      {/* Lien GitHub (placeholder si présent dans le futur) */}
      <Card className="p-5">
        <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 uppercase tracking-wide">
          Ressources
        </h3>
        <p className="mt-3 text-xs text-slate-500 dark:text-slate-500">
          Les liens GitHub, démos et documentation seront affichés ici
          dès qu'ils seront renseignés.
        </p>
        <div className="mt-3 flex items-center gap-1 text-xs text-slate-400 dark:text-slate-600">
          <ExternalLink size={12} />
          <span>À venir</span>
        </div>
      </Card>
    </aside>
  )
}