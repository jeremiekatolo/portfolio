/**
 * Composant placeholder pour les pages en cours de construction.
 *
 * Affiche un titre, une description, et un encadré indiquant que le
 * contenu réel viendra plus tard. Sera remplacé page par page.
 */

interface PagePlaceholderProps {
  title: string
  description: string
}

export function PagePlaceholder({ title, description }: PagePlaceholderProps) {
  return (
    <div className="max-w-4xl mx-auto px-6 py-16">
      <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-slate-100">
        {title}
      </h1>
      <p className="mt-4 text-lg text-slate-600 dark:text-slate-400">
        {description}
      </p>
      <div className="mt-12 p-8 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg">
        <p className="text-sm text-slate-400 dark:text-slate-500">
          Cette page sera complétée aux étapes suivantes de la Phase 4.
        </p>
      </div>
    </div>
  )
}