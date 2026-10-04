import { useEffect } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'

import { LabHeader } from '@/components/labs/LabHeader'
import { LabSection } from '@/components/labs/LabSection'
import { LabSidebar } from '@/components/labs/LabSidebar'
import { Card } from '@/components/ui/Card'
import { laboratoiresApi } from '@/services'

export function LabDetailPage() {
  const { slug } = useParams<{ slug: string }>()

  const { data: lab, isLoading, isError } = useQuery({
    queryKey: ['lab', slug],
    queryFn: () => laboratoiresApi.fetchLaboratoire(slug!),
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

  if (isError || !lab) {
    return (
      <div className="max-w-2xl mx-auto px-6 py-24 text-center">
        <p className="text-6xl font-bold text-sky-500">404</p>
        <h1 className="mt-4 text-2xl font-semibold text-slate-900 dark:text-slate-100">
          Laboratoire introuvable
        </h1>
        <p className="mt-2 text-slate-600 dark:text-slate-400">
          Ce laboratoire n'existe pas, ou n'est pas encore publié.
        </p>
        <Link
          to="/labs"
          className="mt-8 inline-block px-5 py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-medium rounded-lg transition-colors"
        >
          Retour aux laboratoires
        </Link>
      </div>
    )
  }

  // Détermine si au moins une section est remplie
  const aDuContenu =
    lab.objectif ||
    lab.problematique ||
    lab.environnement ||
    lab.architecture_texte ||
    lab.materiel_vm ||
    lab.prerequis ||
    lab.configuration ||
    lab.tests ||
    lab.resultats ||
    lab.incidents_rencontres ||
    lab.corrections ||
    lab.analyse_securite ||
    lab.limites ||
    lab.ameliorations

  return (
    <div className="max-w-6xl mx-auto px-6 py-16">
      <LabHeader lab={lab} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
        <article className="lg:col-span-2">
          {lab.objectif && (
            <LabSection titre="Objectif">{lab.objectif}</LabSection>
          )}

          {lab.problematique && (
            <LabSection titre="Problématique">{lab.problematique}</LabSection>
          )}

          {lab.environnement && (
            <LabSection titre="Environnement">{lab.environnement}</LabSection>
          )}

          {lab.architecture_texte && (
            <LabSection titre="Architecture">
              {lab.architecture_texte}
            </LabSection>
          )}

          {lab.materiel_vm && (
            <LabSection titre="Matériel / VM">{lab.materiel_vm}</LabSection>
          )}

          {lab.prerequis && (
            <LabSection titre="Pré-requis">{lab.prerequis}</LabSection>
          )}

          {lab.configuration && (
            <LabSection titre="Configuration">{lab.configuration}</LabSection>
          )}

          {lab.tests && <LabSection titre="Tests">{lab.tests}</LabSection>}

          {lab.resultats && (
            <LabSection titre="Résultats">{lab.resultats}</LabSection>
          )}

          {lab.incidents_rencontres && (
            <LabSection titre="Incidents rencontrés">
              {lab.incidents_rencontres}
            </LabSection>
          )}

          {lab.corrections && (
            <LabSection titre="Corrections apportées">
              {lab.corrections}
            </LabSection>
          )}

          {lab.analyse_securite && (
            <LabSection titre="Analyse sécurité">
              {lab.analyse_securite}
            </LabSection>
          )}

          {lab.limites && (
            <LabSection titre="Limites">{lab.limites}</LabSection>
          )}

          {lab.ameliorations && (
            <LabSection titre="Améliorations futures">
              {lab.ameliorations}
            </LabSection>
          )}

          {!aDuContenu && (
            <Card className="p-8 text-center">
              <p className="text-slate-500 dark:text-slate-500">
                Le contenu détaillé de ce laboratoire n'est pas encore renseigné.
              </p>
            </Card>
          )}
        </article>

        <LabSidebar lab={lab} />
      </div>
    </div>
  )
}