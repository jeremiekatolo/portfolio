import { Search, X } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'

import { categoriesApi } from '@/services'

export interface FiltresArticles {
  search: string
  categorie: number | ''
}

interface ArticleFiltersProps {
  filtres: FiltresArticles
  onChange: (filtres: FiltresArticles) => void
}

export function ArticleFilters({ filtres, onChange }: ArticleFiltersProps) {
  const { data: categoriesData } = useQuery({
    queryKey: ['categories', 'article'],
    queryFn: () => categoriesApi.fetchCategories({ type: 'article' }),
  })

  const categories = categoriesData?.results ?? []

  const aDesFiltresActifs =
    filtres.search !== '' || filtres.categorie !== ''

  const reinitialiser = () => {
    onChange({ search: '', categorie: '' })
  }

  return (
    <div className="mt-8 p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="relative">
          <Search
            size={16}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />
          <input
            type="text"
            placeholder="Rechercher un article…"
            value={filtres.search}
            onChange={(e) => onChange({ ...filtres, search: e.target.value })}
            className="w-full pl-9 pr-3 py-2 text-sm bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 dark:focus:ring-sky-400 text-slate-900 dark:text-slate-100"
          />
        </div>

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