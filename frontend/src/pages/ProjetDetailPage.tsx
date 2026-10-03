import { useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'

import { ProjetHeader } from '@/components/projets/ProjetHeader'
import { ProjetSection } from '@/components/projets/ProjetSection'
import { ProjetSidebar } from '@/components/projets/ProjetSidebar'
import { Card } from '@/components/ui/Card'
import { projetsApi } from '@/services'

export function ProjetDetailPage() {
  const { slug } = useParams<{ slug: string }>()

  const { data: projet, isLoading, isError } = useQuery({
    queryKey: ['projet', slug],
    queryFn: () => projetsApi.fetchProjet(slug!),
    enabled: !!slug,
    retry: false, // pas de retry en cas de 404
  })

  // Scroll top au changement de projet
  useEffect(() => {
    window.scrollTo(0, 0)
  }, [slug])

  // Chargement
  if (isLoading) {
    return (
      <div className="max-w-5xl mx-auto px-6 py-16">
        <p className="text-slate-500 dark:text-slate-500">Chargement…</p>
      </div>
    )
  }

  // 404 : projet inexistant ou non publié
  if (isError || !projet) {
    return (
      <div className="max-w-2xl mx-auto px-6 py-24 text-center">
        <p className="text-6xl font-bold text-sky-500">404</p>
        <h1 className="mt-4 text-2xl font-semibold text-slate-900 dark:text-slate-100">
          Projet introuvable
        </h1>
        <p className="mt-2 text-slate-600 dark:text-slate-400">
          Ce projet n'existe pas, ou n'est pas encore publié.
        </p>
        <Link
          to="/projets"
          className="mt-8 inline-block px-5 py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-medium rounded-lg transition-colors"
        >
          Retour aux projets
        </Link>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-16">
      <ProjetHeader projet={projet} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
        {/* Colonne principale */}
        <article className="lg:col-span-2">
          {projet.description && (
            <ProjetSection titre="Description">
              {projet.description}
            </ProjetSection>
          )}

          {projet.probleme && (
            <ProjetSection titre="Problème">{projet.probleme}</ProjetSection>
          )}

          {projet.contexte && (
            <ProjetSection titre="Contexte">{projet.contexte}</ProjetSection>
          )}

          {projet.objectifs && (
            <ProjetSection titre="Objectifs">{projet.objectifs}</ProjetSection>
          )}

          {projet.architecture_texte && (
            <ProjetSection titre="Architecture">
              {projet.architecture_texte}
            </ProjetSection>
          )}

          {projet.resultats && (
            <ProjetSection titre="Résultats">{projet.resultats}</ProjetSection>
          )}

          {projet.limites && (
            <ProjetSection titre="Limites">{projet.limites}</ProjetSection>
          )}

          {projet.ameliorations_futures && (
            <ProjetSection titre="Améliorations futures">
              {projet.ameliorations_futures}
            </ProjetSection>
          )}

          {/* Si vraiment aucune section n'a de contenu */}
          {!projet.description &&
            !projet.probleme &&
            !projet.contexte &&
            !projet.objectifs &&
            !projet.architecture_texte &&
            !projet.resultats &&
            !projet.limites &&
            !projet.ameliorations_futures && (
              <Card className="p-8 text-center">
                <p className="text-slate-500 dark:text-slate-500">
                  Le contenu détaillé de ce projet n'est pas encore renseigné.
                </p>
              </Card>
            )}
        </article>

        {/* Sidebar */}
        <ProjetSidebar projet={projet} />
      </div>
    </div>
  )
}