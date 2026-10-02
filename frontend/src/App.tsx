import { useQuery } from '@tanstack/react-query'
import { api } from '@/services'
import type { PaginatedResponse, Projet } from '@/types'

/**
 * Composant racine — version provisoire.
 *
 * Test : récupère la liste des projets publiés depuis l'API Django.
 * Si aucun projet n'existe, l'API renvoie count=0.
 */

function App() {
  const { data, isLoading, isError, error, refetch } = useQuery({
    queryKey: ['projets'],
    queryFn: async () => {
      const response = await api.get<PaginatedResponse<Projet>>(
        '/projets/projets/'
      )
      return response.data
    },
  })

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-6 py-12">
      <div className="max-w-2xl w-full">
        <h1 className="text-4xl font-bold text-slate-900 text-center">
          Test TanStack Query
        </h1>

        <div className="mt-8 p-6 bg-white rounded-lg border border-slate-200 shadow-sm">
          {isLoading && (
            <p className="text-slate-600 text-center">Chargement…</p>
          )}

          {isError && (
            <div className="text-center">
              <p className="text-red-600 font-medium">
                Erreur de chargement
              </p>
              <p className="text-sm text-slate-500 mt-2">
                {error instanceof Error ? error.message : 'Erreur inconnue'}
              </p>
              <p className="text-xs text-slate-400 mt-4">
                Vérifiez que le backend tourne sur
                <code className="ml-1 font-mono">http://localhost:8000</code>
              </p>
            </div>
          )}

          {data && (
            <div className="text-center">
              <p className="text-slate-600">
                Réponse reçue de l&apos;API :
              </p>
              <p className="mt-2 text-3xl font-bold text-sky-500">
                {data.count} projet{data.count > 1 ? 's' : ''}
              </p>
              <button
                onClick={() => refetch()}
                className="mt-6 px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-sm transition-colors"
              >
                Recharger
              </button>
            </div>
          )}
        </div>

        <p className="mt-6 text-xs text-slate-400 text-center">
          Ouvrez la console DevTools (bouton flottant en bas à droite)
          pour explorer le cache TanStack Query.
        </p>
      </div>
    </div>
  )
}

export default App