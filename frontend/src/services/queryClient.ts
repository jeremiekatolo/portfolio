/**
 * Instance unique de QueryClient pour l'application.
 *
 * Configuration par défaut :
 * - staleTime : 5 minutes — les données sont considérées fraîches 5 min
 * - gcTime : 10 minutes — cache conservé 10 min après inutilisation
 * - refetchOnWindowFocus : true — refetch quand l'utilisateur revient sur l'onglet
 * - retry : 1 tentative en cas d'échec réseau (évite les boucles)
 */

import { QueryClient } from '@tanstack/react-query'

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes
      refetchOnWindowFocus: true,
      retry: 1,
    },
    mutations: {
      retry: 0,
    },
  },
})