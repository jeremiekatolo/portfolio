import { Link } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'

export function ContactCTA() {
  return (
    <section className="max-w-7xl mx-auto px-6 py-16">
      <div className="rounded-2xl bg-gradient-to-br from-slate-900 to-slate-800 dark:from-sky-950 dark:to-slate-900 p-10 md:p-14">
        <div className="max-w-2xl">
          <h2 className="text-3xl md:text-4xl font-bold text-white">
            Un projet, une mission, une question ?
          </h2>
          <p className="mt-4 text-slate-300">
            Discutons de vos enjeux réseau, sécurité ou infrastructure.
            Je réponds généralement sous 24h.
          </p>
          <Link
            to="/contact"
            className="mt-8 inline-flex items-center gap-2 px-5 py-3 bg-sky-500 hover:bg-sky-600 text-white font-medium rounded-lg transition-colors"
          >
            Me contacter
            <ArrowRight size={18} />
          </Link>
        </div>
      </div>
    </section>
  )
}