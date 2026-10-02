import { useState } from 'react'

/**
 * Composant racine — version provisoire.
 *
 * Permet de tester :
 * - les polices (Inter, JetBrains Mono)
 * - le mode sombre (bascule manuelle)
 *
 * Ce fichier sera remplacé par le vrai routing à l'Étape 4.7.
 */

function App() {
  const [isDark, setIsDark] = useState(false)

  const toggleTheme = () => {
    const next = !isDark
    setIsDark(next)
    document.documentElement.classList.toggle('dark', next)
  }

  return (
    <div className="min-h-screen bg-slate-50 dark:bg-slate-950 flex items-center justify-center px-6 transition-colors">
      <div className="text-center max-w-2xl">
        <h1 className="text-4xl md:text-5xl font-bold text-slate-900 dark:text-slate-100">
          Portfolio — frontend
        </h1>

        <p className="mt-4 text-slate-600 dark:text-slate-400">
          Tailwind CSS v4 + polices Inter &amp; JetBrains Mono opérationnels.
        </p>

        <p className="mt-6 text-slate-500 dark:text-slate-500">
          Test de la police monospace :{' '}
          <code className="font-mono px-2 py-1 rounded bg-slate-200 dark:bg-slate-800 text-sky-600 dark:text-sky-400 text-sm">
            npm run dev
          </code>
        </p>

        <button
          onClick={toggleTheme}
          className="mt-8 px-5 py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-medium rounded-lg transition-colors"
        >
          Basculer en mode {isDark ? 'clair' : 'sombre'}
        </button>

        <p className="mt-4 text-xs text-slate-400 dark:text-slate-600">
          Le vrai portfolio arrive à l'Étape 4.9.
        </p>
      </div>
    </div>
  )
}

export default App