import { useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'

import { EtudeHeader } from '@/components/etudes/EtudeHeader'
import { EtudeSection } from '@/components/etudes/EtudeSection'
import { EtudeSidebar } from '@/components/etudes/EtudeSidebar'
import { Card } from '@/components/ui/Card'
import { etudesApi } from '@/services'

export function EtudeDetailPage() {
  const { slug } = useParams<{ slug: string }>()

  const { data: etude, isLoading, isError } = useQuery({
    queryKey: ['etude', slug],
    queryFn: () => etudesApi.fetchEtudeDeCas(slug!),
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

  if (isError || !etude) {
    return (
      <div className="max-w-2xl mx-auto px-6 py-24 text-center">
        <p className="text-6xl font-bold text-sky-500">404</p>
        <h1 className="mt-4 text-2xl font-semibold text-slate-900 dark:text-slate-100">
          Étude de cas introuvable
        </h1>
        <p className="mt-2 text-slate-600 dark:text-slate-400">
          Cette étude n'existe pas, ou n'est pas encore publiée.
        </p>
        <Link
          to="/etudes-de-cas"
          className="mt-8 inline-block px-5 py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-medium rounded-lg transition-colors"
        >
          Retour aux études de cas
        </Link>
      </div>
    )
  }

  const aDuContenu =
    etude.probleme ||
    etude.contexte ||
    etude.analyse ||
    etude.exigences ||
    etude.menaces ||
    etude.architecture_texte ||
    etude.choix_techniques ||
    etude.implementation ||
    etude.securisation ||
    etude.tests ||
    etude.resultats ||
    etude.limites ||
    etude.recommandations

  return (
    <div className="max-w-6xl mx-auto px-6 py-16">
      <EtudeHeader etude={etude} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <article className="lg:col-span-2">
          {etude.probleme && (
            <EtudeSection titre="Problème">{etude.probleme}</EtudeSection>
          )}
          {etude.contexte && (
            <EtudeSection titre="Contexte">{etude.contexte}</EtudeSection>
          )}
          {etude.analyse && (
            <EtudeSection titre="Analyse">{etude.analyse}</EtudeSection>
          )}
          {etude.exigences && (
            <EtudeSection titre="Exigences">{etude.exigences}</EtudeSection>
          )}
          {etude.menaces && (
            <EtudeSection titre="Menaces">{etude.menaces}</EtudeSection>
          )}
          {etude.architecture_texte && (
            <EtudeSection titre="Architecture">
              {etude.architecture_texte}
            </EtudeSection>
          )}
          {etude.choix_techniques && (
            <EtudeSection titre="Choix techniques">
              {etude.choix_techniques}
            </EtudeSection>
          )}
          {etude.implementation && (
            <EtudeSection titre="Implémentation">
              {etude.implementation}
            </EtudeSection>
          )}
          {etude.securisation && (
            <EtudeSection titre="Sécurisation">
              {etude.securisation}
            </EtudeSection>
          )}
          {etude.tests && <EtudeSection titre="Tests">{etude.tests}</EtudeSection>}
          {etude.resultats && (
            <EtudeSection titre="Résultats">{etude.resultats}</EtudeSection>
          )}
          {etude.limites && (
            <EtudeSection titre="Limites">{etude.limites}</EtudeSection>
          )}
          {etude.recommandations && (
            <EtudeSection titre="Recommandations">
              {etude.recommandations}
            </EtudeSection>
          )}

          {!aDuContenu && (
            <Card className="p-8 text-center">
              <p className="text-slate-500 dark:text-slate-500">
                Le contenu détaillé de cette étude de cas n'est pas encore renseigné.
              </p>
            </Card>
          )}
        </article>

        <EtudeSidebar etude={etude} />
      </div>
    </div>
  )
}