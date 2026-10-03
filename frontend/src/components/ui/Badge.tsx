import type { ReactNode } from 'react'

type BadgeVariant = 'default' | 'sky' | 'green' | 'amber'

interface BadgeProps {
  children: ReactNode
  variant?: BadgeVariant
}

const VARIANT_CLASSES: Record<BadgeVariant, string> = {
  default:
    'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300',
  sky: 'bg-sky-100 text-sky-700 dark:bg-sky-950 dark:text-sky-300',
  green:
    'bg-emerald-100 text-emerald-700 dark:bg-emerald-950 dark:text-emerald-300',
  amber:
    'bg-amber-100 text-amber-700 dark:bg-amber-950 dark:text-amber-300',
}

export function Badge({ children, variant = 'default' }: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 text-xs font-medium rounded ${VARIANT_CLASSES[variant]}`}
    >
      {children}
    </span>
  )
}