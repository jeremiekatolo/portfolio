import { Search, X } from 'lucide-react'

export interface FiltresLabs {
  search: string
  difficulte: string
}

interface LabFiltersProps {
  filtres: FiltresLabs
  onChange: (filtres: FiltresLabs) => void
}

const DIFFICULTES = [
  { value: '', label: 'Toutes les difficultés' },
  { value: 'debutant', label: 'Débutant' },
  { value: 'intermediaire', label: 'Intermédiaire' },
  { value: 'avance', label: 'Avancé' },
  { value: 'expert', label: 'Expert' },
]

export function LabFilters({ filtres, onChange }: LabFiltersProps) {
  const aDesFiltresActifs =
    filtres.search !== '' || filtres.difficulte !== ''

  const reinitialiser = () => {
    onChange({ search: '', difficulte: '' })
  }

  return (
    <div className="mt-8 p-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {/* Recherche */}
        <div className="relative">
          <Search
            size={16}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />
          <input
            type="text"
            placeholder="Rechercher un laboratoire…"
            value={filtres.search}
            onChange={(e) => onChange({ ...filtres, search: e.target.value })}
            className="w-full pl-9 pr-3 py-2 text-sm bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 dark:focus:ring-sky-400 text-slate-900 dark:text-slate-100"
          />
        </div>

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