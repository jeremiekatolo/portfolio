import { useQuery } from '@tanstack/react-query'

import { Badge } from '@/components/ui/Badge'
import { Card } from '@/components/ui/Card'
import { competencesApi } from '@/services'
import type { Competence } from '@/types'

const DOMAINE_LABEL: Record<string, string> = {
  reseaux: 'Réseaux',
  cybersecurite: 'Cybersécurité',
  systemes: 'Systèmes',
  automatisation: 'Automatisation',
  developpement: 'Développement',
}

export function CompetencesCles() {
  const { data, isLoading } = useQuery({
    queryKey: ['competences'],
    queryFn: () => competencesApi.fetchCompetences(),
  })

  const competences = data?.results ?? []

  // Groupe par domaine
  const parDomaine = competences.reduce<Record<string, Competence[]>>(
    (acc, comp) => {
      acc[comp.domaine] = acc[comp.domaine] ?? []
      acc[comp.domaine].push(comp)
      return acc
    },
    {}
  )

  return (
    <section className="max-w-7xl mx-auto px-6 py-16">
      <h2 className="text-3xl font-bold text-slate-900 dark:text-slate-100">
        Compétences clés
      </h2>
      <p className="mt-2 text-slate-600 dark:text-slate-400">
        Chaque compétence est reliée à des projets et laboratoires concrets.
      </p>

      {isLoading && (
        <p className="mt-10 text-slate-500 dark:text-slate-500">
          Chargement…
        </p>
      )}

      {!isLoading && competences.length === 0 && (
        <Card className="mt-10 p-8 text-center">
          <p className="text-slate-500 dark:text-slate-500">
            Aucune compétence enregistrée pour l&apos;instant.
          </p>
        </Card>
      )}

      {competences.length > 0 && (
        <div className="mt-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(parDomaine).map(([domaine, items]) => (
            <Card key={domaine} className="p-6">
              <h3 className="font-semibold text-slate-900 dark:text-slate-100">
                {DOMAINE_LABEL[domaine] ?? domaine}
              </h3>
              <div className="mt-4 flex flex-wrap gap-2">
                {items.map((comp) => (
                  <Badge key={comp.id} variant="default">
                    {comp.nom}
                  </Badge>
                ))}
              </div>
            </Card>
          ))}
        </div>
      )}
    </section>
  )
}