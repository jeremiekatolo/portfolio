import type { ReactNode } from 'react'

interface EtudeSectionProps {
  titre: string
  children: ReactNode
}

export function EtudeSection({ titre, children }: EtudeSectionProps) {
  return (
    <section className="mt-10 first:mt-0">
      <h2 className="text-2xl font-bold text-slate-900 dark:text-slate-100">
        {titre}
      </h2>
      <div className="mt-4 prose prose-slate dark:prose-invert max-w-none whitespace-pre-line text-slate-700 dark:text-slate-300 leading-relaxed">
        {children}
      </div>
    </section>
  )
}