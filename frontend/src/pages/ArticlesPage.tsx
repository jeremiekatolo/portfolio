import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'

import { ArticleCard } from '@/components/articles/ArticleCard'
import { ArticleFilters, type FiltresArticles } from '@/components/articles/ArticleFilters'
import { Card } from '@/components/ui/Card'
import { articlesApi } from '@/services'

const FILTRES_INITIAUX: FiltresArticles = {
  search: '',
  categorie: '',
}

export function ArticlesPage() {
  const [filtres, setFiltres] = useState<FiltresArticles>(FILTRES_INITIAUX)

  const { data, isLoading, isError } = useQuery({
    queryKey: ['articles', filtres],
    queryFn: () =>
      articlesApi.fetchArticles({
        search: filtres.search || undefined,
        categorie: filtres.categorie || undefined,
      }),
  })

  const articles = data?.results ?? []
  const total = data?.count ?? 0

  return (
    <div className="max-w-7xl mx-auto px-6 py-16">
      <div>
        <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-slate-100">
          Articles
        </h1>
        <p className="mt-4 text-lg text-slate-600 dark:text-slate-400">
          Analyses techniques, retours d'expérience et veille technologique.
        </p>
      </div>

      <ArticleFilters filtres={filtres} onChange={setFiltres} />

      {!isLoading && !isError && (
        <p className="mt-6 text-sm text-slate-500 dark:text-slate-500">
          {total} article{total > 1 ? 's' : ''} trouvé{total > 1 ? 's' : ''}
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

      {!isLoading && !isError && articles.length === 0 && (
        <Card className="mt-8 p-12 text-center">
          <p className="text-slate-500 dark:text-slate-500">
            {total === 0
              ? 'Aucun article publié pour l’instant.'
              : 'Aucun article ne correspond à ces filtres.'}
          </p>
          <p className="mt-2 text-sm text-slate-400 dark:text-slate-600">
            {total === 0
              ? 'Connectez-vous à l’admin Django pour ajouter des articles.'
              : 'Essayez de réinitialiser les filtres.'}
          </p>
        </Card>
      )}

      {articles.length > 0 && (
        <div className="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {articles.map((article) => (
            <ArticleCard key={article.id} article={article} />
          ))}
        </div>
      )}
    </div>
  )
}