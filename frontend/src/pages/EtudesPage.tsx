import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'

import { EtudeCard } from '@/components/etudes/EtudeCard'
import { EtudeFilters, type FiltresEtudes } from '@/components/etudes/EtudeFilters'
import { Card } from '@/components/ui/Card'
import { etudesApi } from '@/services'

const FILTRES_INITIAUX: FiltresEtudes = { search: '' }

export function EtudesPage() {
  const [filtres, setFiltres] = useState<FiltresEtudes>(FILTRES_INITIAUX)

  const { data, isLoading, isError } = useQuery({
    queryKey: ['etudes', filtres],
    queryFn: () =>
      etudesApi.fetchEtudesDeCas({
        search: filtres.search || undefined,
      }),
  })

  const etudes = data?.results ?? []
  const total = data?.count ?? 0

  return (
    <div className="max-w-7xl mx-auto px-6 py-16">
      <div>
        <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-slate-100">
          Études de cas
        </h1>
        <p className="mt-4 text-lg text-slate-600 dark:text-slate-400">
          Analyses structurées : problème, contexte, architecture, menaces,
          résultats, recommandations.
        </p>
      </div>

      <EtudeFilters filtres={filtres} onChange={setFiltres} />

      {!isLoading && !isError && (
        <p className="mt-6 text-sm text-slate-500 dark:text-slate-500">
          {total} étude{total > 1 ? 's' : ''} trouvée{total > 1 ? 's' : ''}
        </p>
      )}

      {isLoading && (
        <p className="mt-8 text-slate-500 dark:text-slate-500">Chargement…</p>
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

      {!isLoading && !isError && etudes.length === 0 && (
        <Card className="mt-8 p-12 text-center">
          <p className="text-slate-500 dark:text-slate-500">
            {total === 0
              ? 'Aucune étude de cas publiée pour l’instant.'
              : 'Aucune étude ne correspond à ces filtres.'}
          </p>
          <p className="mt-2 text-sm text-slate-400 dark:text-slate-600">
            {total === 0
              ? 'Connectez-vous à l’admin Django pour ajouter des études de cas.'
              : 'Essayez de réinitialiser la recherche.'}
          </p>
        </Card>
      )}

      {etudes.length > 0 && (
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {etudes.map((etude) => (
            <EtudeCard key={etude.id} etude={etude} />
          ))}
        </div>
      )}
    </div>
  )
}