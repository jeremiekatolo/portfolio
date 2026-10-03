import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'

import { ProjetCard } from '@/components/projets/ProjetCard'
import { ProjetFilters, type FiltresProjets } from '@/components/projets/ProjetFilters'
import { Card } from '@/components/ui/Card'
import { projetsApi } from '@/services'

const FILTRES_INITIAUX: FiltresProjets = {
  search: '',
  categorie: '',
  difficulte: '',
}

export function ProjetsPage() {
  const [filtres, setFiltres] = useState<FiltresProjets>(FILTRES_INITIAUX)

  const { data, isLoading, isError } = useQuery({
    queryKey: ['projets', filtres],
    queryFn: () =>
      projetsApi.fetchProjets({
        search: filtres.search || undefined,
        categorie: filtres.categorie || undefined,
        difficulte: filtres.difficulte || undefined,
      }),
  })

  const projets = data?.results ?? []
  const total = data?.count ?? 0

  return (
    <div className="max-w-7xl mx-auto px-6 py-16">
      {/* En-tête */}
      <div>
        <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-slate-100">
          Projets
        </h1>
        <p className="mt-4 text-lg text-slate-600 dark:text-slate-400">
          Réalisations techniques : réseau, cybersécurité, infrastructure,
          automatisation.
        </p>
      </div>

      {/* Filtres */}
      <ProjetFilters filtres={filtres} onChange={setFiltres} />

      {/* Compteur */}
      {!isLoading && !isError && (
        <p className="mt-6 text-sm text-slate-500 dark:text-slate-500">
          {total} projet{total > 1 ? 's' : ''} trouvé{total > 1 ? 's' : ''}
        </p>
      )}

      {/* États */}
      {isLoading && (
        <p className="mt-8 text-slate-500 dark:text-slate-500">
          Chargement…
        </p>
      )}

      {isError && (
        <Card className="mt-8 p-8 text-center">
          <p className="text-red-600 dark:text-red-400 font-medium">
            Erreur de chargement
          </p>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-500">
            Vérifiez que le backend tourne.
          </p>
        </Card>
      )}

      {!isLoading && !isError && projets.length === 0 && (
        <Card className="mt-8 p-12 text-center">
          <p className="text-slate-500 dark:text-slate-500">
            {total === 0
              ? 'Aucun projet publié pour l’instant.'
              : 'Aucun projet ne correspond à ces filtres.'}
          </p>
          <p className="mt-2 text-sm text-slate-400 dark:text-slate-600">
            {total === 0
              ? 'Connectez-vous à l’admin Django pour ajouter des projets.'
              : 'Essayez de réinitialiser les filtres.'}
          </p>
        </Card>
      )}

      {/* Grille */}
      {projets.length > 0 && (
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {projets.map((projet) => (
            <ProjetCard key={projet.id} projet={projet} />
          ))}
        </div>
      )}
    </div>
  )
}