import { api } from './client'
import type { Laboratoire, PaginatedResponse } from '@/types'

export interface LaboratoiresFilters {
  difficulte?: string
  search?: string
}

export async function fetchLaboratoires(
  filters: LaboratoiresFilters = {}
): Promise<PaginatedResponse<Laboratoire>> {
  const params = new URLSearchParams()
  if (filters.difficulte) params.set('difficulte', filters.difficulte)
  if (filters.search) params.set('search', filters.search)

  const query = params.toString()
  const url = `/laboratoires/laboratoires/${query ? `?${query}` : ''}`
  const response = await api.get<PaginatedResponse<Laboratoire>>(url)
  return response.data
}

export async function fetchLaboratoire(slug: string): Promise<Laboratoire> {
  const response = await api.get<Laboratoire>(
    `/laboratoires/laboratoires/${slug}/`
  )
  return response.data
}