import { Search, X } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'

import { categoriesApi } from '@/services'

export interface FiltresProjets {
  search: string
  categorie: number | ''
  difficulte: string
}

interface ProjetFiltersProps {
  filtres: FiltresProjets
  onChange: (filtres: FiltresProjets) => void
}

const DIFFICULTES = [
  { value: '', label: 'Toutes les difficultés' },
  { value: 'debutant', label: 'Débutant' },
  { value: 'intermediaire', label: 'Intermédiaire' },
  { value: 'avance', label: 'Avancé' },
  { value: 'expert', label: 'Expert' },
]

export function ProjetFilters({ filtres, onChange }: ProjetFiltersProps) {
  const { data: categoriesData } = useQuery({
    queryKey: ['categories', 'projet'],
    queryFn: async () => {
      const response = await categoriesApi.fetchCategories({ type: 'projet' })
      return response
    },
  })

  const categories = categoriesData?.results ?? []

  const aDesFiltresActifs =
    filtres.search !== '' ||
    filtres.categorie !== '' ||
    filtres.difficulte !== ''

  const reinitialiser = () => {
    onChange({ search: '', categorie: '', difficulte: '' })
  }

  return (
    <div className="mt-8 p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {/* Recherche */}
        <div className="relative">
          <Search
            size={16}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />
          <input
            type="text"
            placeholder="Rechercher un projet…"
            value={filtres.search}
            onChange={(e) => onChange({ ...filtres, search: e.target.value })}
            className="w-full pl-9 pr-3 py-2 text-sm bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 dark:focus:ring-sky-400 text-slate-900 dark:text-slate-100"
          />
        </div>

        {/* Catégorie */}
        <select
          value={filtres.categorie}
          onChange={(e) =>
            onChange({
              ...filtres,
              categorie: e.target.value ? Number(e.target.value) : '',
            })
          }
          className="px-3 py-2 text-sm bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 dark:focus:ring-sky-400 text-slate-900 dark:text-slate-100"
        >
          <option value="">Toutes les catégories</option>
          {categories.map((cat) => (
            <option key={cat.id} value={cat.id}>
              {cat.nom}
            </option>
          ))}
        </select>

        {/* Difficulté */}
        <select
          value={filtres.difficulte}
          onChange={(e) =>
            onChange({ ...filtres, difficulte: e.target.value })
          }
          className="px-3 py-2 text-sm bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 dark:focus:ring-sky-400 text-slate-900 dark:text-slate-100"
        >
          {DIFFICULTES.map((d) => (
            <option key={d.value} value={d.value}>
              {d.label}
            </option>
          ))}
        </select>
      </div>

      {aDesFiltresActifs && (
        <button
          type="button"
          onClick={reinitialiser}
          className="mt-3 inline-flex items-center gap-1 text-xs text-slate-500 dark:text-slate-500 hover:text-slate-900 dark:hover:text-slate-100 transition-colors"
        >
          <X size={14} />
          Réinitialiser les filtres
        </button>
      )}
    </div>
  )
}