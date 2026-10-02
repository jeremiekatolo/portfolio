export function Footer() {
  const year = new Date().getFullYear()

  return (
    <footer className="border-t border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900">
      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <p className="text-sm text-slate-500 dark:text-slate-500">
            © {year} Jeremie Katolo — Ingénieur Réseaux &amp; Cybersécurité
          </p>
          <p className="text-xs text-slate-400 dark:text-slate-600 text-center md:text-right">
            Construit avec React, TypeScript, Tailwind CSS et Django REST Framework.
          </p>
        </div>
      </div>
    </footer>
  )
}