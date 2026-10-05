import { useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'

import { ArticleHeader } from '@/components/articles/ArticleHeader'
import { ArticleSidebar } from '@/components/articles/ArticleSidebar'
import { Card } from '@/components/ui/Card'
import { articlesApi } from '@/services'

export function ArticleDetailPage() {
  const { slug } = useParams<{ slug: string }>()

  const { data: article, isLoading, isError } = useQuery({
    queryKey: ['article', slug],
    queryFn: () => articlesApi.fetchArticle(slug!),
    enabled: !!slug,
    retry: false,
  })

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [slug])

  if (isLoading) {
    return (
      <div className="max-w-5xl mx-auto px-6 py-16">
        <p className="text-slate-500 dark:text-slate-500">Chargement…</p>
      </div>
    )
  }

  if (isError || !article) {
    return (
      <div className="max-w-2xl mx-auto px-6 py-24 text-center">
        <p className="text-6xl font-bold text-sky-500">404</p>
        <h1 className="mt-4 text-2xl font-semibold text-slate-900 dark:text-slate-100">
          Article introuvable
        </h1>
        <p className="mt-2 text-slate-600 dark:text-slate-400">
          Cet article n'existe pas, ou n'est pas encore publié.
        </p>
        <Link
          to="/articles"
          className="mt-8 inline-block px-5 py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-medium rounded-lg transition-colors"
        >
          Retour aux articles
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-16">
      <ArticleHeader article={article} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <article className="lg:col-span-2">
          {article.contenu ? (
            <div className="prose prose-slate dark:prose-invert max-w-none whitespace-pre-line text-slate-700 dark:text-slate-300 leading-relaxed">
              {article.contenu}
            </div>
          ) : (
            <Card className="p-8 text-center">
              <p className="text-slate-500 dark:text-slate-500">
                Le contenu de cet article n'est pas encore renseigné.
              </p>
            </Card>
          )}
        </article>

        <ArticleSidebar article={article} />
      </div>
    </div>
  )
}