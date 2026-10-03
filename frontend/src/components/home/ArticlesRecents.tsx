import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import { ArrowRight, Clock } from 'lucide-react'

import { Badge } from '@/components/ui/Badge'
import { Card } from '@/components/ui/Card'
import { articlesApi } from '@/services'

export function ArticlesRecents() {
  const { data, isLoading } = useQuery({
    queryKey: ['articles', 'recents'],
    queryFn: () => articlesApi.fetchArticles(),
  })

  const articles = data?.results.slice(0, 3) ?? []

  return (
    <section className="max-w-7xl mx-auto px-6 py-16">
      <div className="flex items-end justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold text-slate-900 dark:text-slate-100">
            Derniers articles
          </h2>
          <p className="mt-2 text-slate-600 dark:text-slate-400">
            Analyses techniques, retours d&apos;expérience et veille.
          </p>
        </div>
        <Link
          to="/articles"
          className="hidden md:inline-flex items-center gap-1 text-sm font-medium text-sky-600 dark:text-sky-400 hover:underline"
        >
          Voir tous les articles
          <ArrowRight size={16} />
        </Link>
      </div>

      {isLoading && (
        <p className="mt-10 text-slate-500 dark:text-slate-500">
          Chargement…
        </p>
      )}

      {!isLoading && articles.length === 0 && (
        <Card className="mt-10 p-8 text-center">
          <p className="text-slate-500 dark:text-slate-500">
            Aucun article publié pour l&apos;instant.
          </p>
        </Card>
      )}

      {articles.length > 0 && (
        <div className="mt-10 grid grid-cols-1 md:grid-cols-3 gap-4">
          {articles.map((article) => (
            <Card key={article.id} className="p-6 flex flex-col">
              <Badge variant="sky">{article.categorie.nom}</Badge>
              <h3 className="mt-4 text-lg font-semibold text-slate-900 dark:text-slate-100 line-clamp-2">
                {article.titre}
              </h3>
              <p className="mt-2 text-sm text-slate-600 dark:text-slate-400 line-clamp-3 flex-1">
                {article.resume}
              </p>
              <div className="mt-4 flex items-center justify-between text-xs text-slate-400 dark:text-slate-500">
                <span className="inline-flex items-center gap-1">
                  <Clock size={12} />
                  {article.temps_lecture} min
                </span>
                <Link
                  to={`/articles/${article.slug}`}
                  className="font-medium text-sky-600 dark:text-sky-400 hover:underline"
                >
                  Lire
                </Link>
              </div>
            </Card>
          ))}
        </div>
      )}
    </section>
  )
}