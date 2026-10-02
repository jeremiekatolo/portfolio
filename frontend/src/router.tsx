import { createBrowserRouter } from 'react-router-dom'

import { MainLayout } from '@/layouts/MainLayout'
import { HomePage } from '@/pages/HomePage'
import { ProjetsPage } from '@/pages/ProjetsPage'
import { LabsPage } from '@/pages/LabsPage'
import { EtudesPage } from '@/pages/EtudesPage'
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
      { path: 'labs', element: <LabsPage /> },
      { path: 'etudes-de-cas', element: <EtudesPage /> },
      { path: 'articles', element: <ArticlesPage /> },
      { path: 'parcours', element: <ParcoursPage /> },
      { path: 'a-propos', element: <AProposPage /> },
      { path: 'contact', element: <ContactPage /> },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])