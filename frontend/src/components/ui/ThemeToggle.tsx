import { Moon, Sun, Monitor } from 'lucide-react'

import { useTheme } from '@/hooks/useTheme'
import type { ThemeMode } from '@/contexts/ThemeContext'

const OPTIONS: { value: ThemeMode; label: string; Icon: typeof Sun }[] = [
  { value: 'clair', label: 'Clair', Icon: Sun },
  { value: 'systeme', label: 'Système', Icon: Monitor },
  { value: 'sombre', label: 'Sombre', Icon: Moon },
]

export function ThemeToggle() {
  const { mode, setMode } = useTheme()

  return (
    <div
      role="group"
      aria-label="Choix du thème"
      className="inline-flex items-center rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-0.5"
    >
      {OPTIONS.map(({ value, label, Icon }) => {
        const actif = mode === value
        return (
          <button
            key={value}
            type="button"
            onClick={() => setMode(value)}
            aria-label={`Thème ${label}`}
            aria-pressed={actif}
            title={label}
            className={[
              'p-1.5 rounded-md transition-colors',
              actif
                ? 'bg-sky-500 text-white'
                : 'text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800',
            ].join(' ')}
          >
            <Icon size={16} />
          </button>
        )
      })}
    </div>
  )
}