import { Link } from 'react-router-dom'

export function NotFoundPage() {
  return (
    <div className="max-w-2xl mx-auto px-6 py-24 text-center">
      <p className="text-6xl font-bold text-sky-500">404</p>
      <h1 className="mt-4 text-2xl font-semibold text-slate-900 dark:text-slate-100">
        Page introuvable
      </h1>
      <p className="mt-2 text-slate-600 dark:text-slate-400">
        La page que vous cherchez n'existe pas ou a été déplacée.
      </p>
      <Link
        to="/"
        className="mt-8 inline-block px-5 py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-medium rounded-lg transition-colors"
      >
        Retour à l'accueil
      </Link>
    </div>
  )
}