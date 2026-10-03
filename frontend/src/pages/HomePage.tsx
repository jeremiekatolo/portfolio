import { Hero } from '@/components/home/Hero'
import { Domaines } from '@/components/home/Domaines'
import { ProjetsRecents } from '@/components/home/ProjetsRecents'
import { CompetencesCles } from '@/components/home/CompetencesCles'
import { ArticlesRecents } from '@/components/home/ArticlesRecents'
import { ContactCTA } from '@/components/home/ContactCTA'

export function HomePage() {
  return (
    <>
      <Hero />
      <Domaines />
      <ProjetsRecents />
      <CompetencesCles />
      <ArticlesRecents />
      <ContactCTA />
    </>
  )
}