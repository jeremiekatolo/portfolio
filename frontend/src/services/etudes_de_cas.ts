import { api } from './client'
import type { EtudeDeCas, PaginatedResponse } from '@/types'

export interface EtudesFilters {
  search?: string
}

export async function fetchEtudesDeCas(
  filters: EtudesFilters = {}
): Promise<PaginatedResponse<EtudeDeCas>> {
  const params = new URLSearchParams()
  if (filters.search) params.set('search', filters.search)

  const query = params.toString()
  const url = `/etudes-de-cas/etudes-de-cas/${query ? `?${query}` : ''}`
  const response = await api.get<PaginatedResponse<EtudeDeCas>>(url)
  return response.data
}

export async function fetchEtudeDeCas(slug: string): Promise<EtudeDeCas> {
  const response = await api.get<EtudeDeCas>(
    `/etudes-de-cas/etudes-de-cas/${slug}/`
  )
  return response.data
}