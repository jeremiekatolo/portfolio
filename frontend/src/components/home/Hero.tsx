import { Link } from 'react-router-dom'
import { ArrowRight, Mail } from 'lucide-react'

import { Badge } from '@/components/ui/Badge'

export function Hero() {
  return (
    <section className="relative overflow-hidden">
      <div className="max-w-7xl mx-auto px-6 py-20 md:py-32">
        <div className="max-w-3xl">
          <Badge variant="sky">
            <span className="inline-block w-2 h-2 rounded-full bg-sky-500 mr-2" />
            Disponible pour missions
          </Badge>

          <h1 className="mt-6 text-4xl md:text-6xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
            Jeremie Katolo
          </h1>

          <p className="mt-4 text-xl md:text-2xl text-sky-600 dark:text-sky-400 font-medium">
            Network &amp; Cybersecurity Engineer
          </p>

          <p className="mt-6 text-lg text-slate-600 dark:text-slate-400 max-w-2xl">
            Je conçois, sécurise et documente des infrastructures réseau
            et des systèmes exposés, avec une approche d&apos;ingénierie
            vérifiable : analyse, architecture, implémentation, tests,
            supervision et amélioration continue.
          </p>

          <div className="mt-10 flex flex-wrap gap-4">
            <Link
              to="/projets"
              className="inline-flex items-center gap-2 px-5 py-3 bg-sky-500 hover:bg-sky-600 text-white font-medium rounded-lg transition-colors"
            >
              Voir mes projets
              <ArrowRight size={18} />
            </Link>
            <Link
              to="/contact"
              className="inline-flex items-center gap-2 px-5 py-3 bg-white dark:bg-slate-900 hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-900 dark:text-slate-100 font-medium rounded-lg border border-slate-200 dark:border-slate-800 transition-colors"
            >
              <Mail size={18} />
              Me contacter
            </Link>
          </div>
        </div>
      </div>
    </section>
  )
}