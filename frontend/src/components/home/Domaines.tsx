import { Network, Shield, Server, Terminal } from 'lucide-react'

import { Card } from '@/components/ui/Card'

const DOMAINES = [
  {
    icon: Network,
    titre: 'Réseaux',
    description:
      'TCP/IP, routing, switching, VLAN, NAT, VPN, firewalls, segmentation.',
  },
  {
    icon: Shield,
    titre: 'Cybersécurité',
    description:
      'Sécurité réseau, sécurité web, authentification, cryptographie, SOC, hardening.',
  },
  {
    icon: Server,
    titre: 'Systèmes',
    description:
      'Linux, services, administration, durcissement, supervision.',
  },
  {
    icon: Terminal,
    titre: 'Automatisation',
    description:
      'Python, Bash, APIs, CI/CD, scripts d’exploitation et d’audit.',
  },
]

export function Domaines() {
  return (
    <section className="max-w-7xl mx-auto px-6 py-16">
      <h2 className="text-3xl font-bold text-slate-900 dark:text-slate-100">
        Domaines d&apos;expertise
      </h2>
      <p className="mt-2 text-slate-600 dark:text-slate-400">
        Quatre piliers au service de l&apos;ingénierie réseau et sécurité.
      </p>

      <div className="mt-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {DOMAINES.map(({ icon: Icon, titre, description }) => (
          <Card key={titre} className="p-6">
            <div className="w-10 h-10 rounded-lg bg-sky-100 dark:bg-sky-950 flex items-center justify-center">
              <Icon
                size={20}
                className="text-sky-600 dark:text-sky-400"
              />
            </div>
            <h3 className="mt-4 font-semibold text-slate-900 dark:text-slate-100">
              {titre}
            </h3>
            <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
              {description}
            </p>
          </Card>
        ))}
      </div>
    </section>
  )
}