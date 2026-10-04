import { createBrowserRouter } from 'react-router-dom'

import { MainLayout } from '@/layouts/MainLayout'
import { HomePage } from '@/pages/HomePage'
import { ProjetsPage } from '@/pages/ProjetsPage'
import { ProjetDetailPage } from '@/pages/ProjetDetailPage'
import { LabsPage } from '@/pages/LabsPage'
import { LabDetailPage } from '@/pages/LabDetailPage'
import { EtudesPage } from '@/pages/EtudesPage'
import { EtudeDetailPage } from '@/pages/EtudeDetailPage'
import { ArticlesPage } from '@/pages/ArticlesPage'
import { ParcoursPage } from '@/pages/ParcoursPage'
import { AProposPage } from '@/pages/AProposPage'
import { ContactPage } from '@/pages/ContactPage'
import { NotFoundPage } from '@/pages/NotFoundPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'projets', element: <ProjetsPage /> },
      { path: 'projets/:slug', element: <ProjetDetailPage /> },
      { path: 'labs', element: <LabsPage /> },
      { path: 'labs/:slug', element: <LabDetailPage /> },
      { path: 'etudes-de-cas', element: <EtudesPage /> },
      { path: 'etudes-de-cas/:slug', element: <EtudeDetailPage /> },
      { path: 'articles', element: <ArticlesPage /> },
      { path: 'parcours', element: <ParcoursPage /> },
      { path: 'a-propos', element: <AProposPage /> },
      { path: 'contact', element: <ContactPage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])