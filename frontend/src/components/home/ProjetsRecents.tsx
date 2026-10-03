import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ArrowRight } from 'lucide-react'

import { Badge } from '@/components/ui/Badge'
import { Card } from '@/components/ui/Card'
import { projetsApi } from '@/services'

export function ProjetsRecents() {
  const { data, isLoading } = useQuery({
    queryKey: ['projets', 'recents'],
    queryFn: () => projetsApi.fetchProjets(),
  })

  const projets = data?.results.slice(0, 3) ?? []

  return (
    <section className="max-w-7xl mx-auto px-6 py-16">
      <div className="flex items-end justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold text-slate-900 dark:text-slate-100">
            Projets récents
          </h2>
          <p className="mt-2 text-slate-600 dark:text-slate-400">
            Une sélection de projets techniques publiés.
          </p>
        </div>
        <Link
          to="/projets"
          className="hidden md:inline-flex items-center gap-1 text-sm font-medium text-sky-600 dark:text-sky-400 hover:underline"
        >
          Voir tous les projets
          <ArrowRight size={16} />
        </Link>
      </div>

      {isLoading && (
        <p className="mt-10 text-slate-500 dark:text-slate-500">
          Chargement…
        </p>
      )}

      {!isLoading && projets.length === 0 && (
        <Card className="mt-10 p-8 text-center">
          <p className="text-slate-500 dark:text-slate-500">
            Aucun projet publié pour l&apos;instant.
          </p>
          <p className="mt-2 text-sm text-slate-400 dark:text-slate-600">
            Connectez-vous à l&apos;admin Django pour ajouter des projets.
          </p>
        </Card>
      )}

      {projets.length > 0 && (
        <div className="mt-10 grid grid-cols-1 md:grid-cols-3 gap-4">
          {projets.map((projet) => (
            <Card key={projet.id} className="p-6 flex flex-col">
              <div className="flex flex-wrap gap-2">
                <Badge variant="sky">{projet.categorie.nom}</Badge>
                <Badge>{projet.difficulte_display}</Badge>
              </div>
              <h3 className="mt-4 text-lg font-semibold text-slate-900 dark:text-slate-100 line-clamp-2">
                {projet.titre}
              </h3>
              <p className="mt-2 text-sm text-slate-600 dark:text-slate-400 line-clamp-3 flex-1">
                {projet.resume || projet.description.slice(0, 150)}
              </p>
              <Link
                to={`/projets/${projet.slug}`}
                className="mt-4 inline-flex items-center gap-1 text-sm font-medium text-sky-600 dark:text-sky-400 hover:underline"
              >
                Découvrir
                <ArrowRight size={14} />
              </Link>
            </Card>
          ))}
        </div>
      )}
    </section>
  )
}