import { Search, X } from 'lucide-react'

export interface FiltresEtudes {
  search: string
}

interface EtudeFiltersProps {
  filtres: FiltresEtudes
  onChange: (filtres: FiltresEtudes) => void
}

export function EtudeFilters({ filtres, onChange }: EtudeFiltersProps) {
  const aDesFiltresActifs = filtres.search !== ''

  return (
    <div className="mt-8 p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg">
      <div className="relative">
        <Search
          size={16}
          className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
        />
        <input
          type="text"
          placeholder="Rechercher une étude de cas…"
          value={filtres.search}
          onChange={(e) => onChange({ search: e.target.value })}
          className="w-full pl-9 pr-3 py-2 text-sm bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 dark:focus:ring-sky-400 text-slate-900 dark:text-slate-100"
        />
      </div>

      {aDesFiltresActifs && (
        <button
          type="button"
          onClick={() => onChange({ search: '' })}
          className="mt-3 inline-flex items-center gap-1 text-xs text-slate-500 dark:text-slate-500 hover:text-slate-900 dark:hover:text-slate-100 transition-colors"
        >
          <X size={14} />
          Réinitialiser la recherche
        </button>
      )}
    </div>
  )
}