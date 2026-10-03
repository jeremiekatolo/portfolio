import { api } from './client'
import type { PaginatedResponse, Projet } from '@/types'

export interface ProjetsFilters {
  categorie?: number
  difficulte?: string
  mis_en_avant?: boolean
  search?: string
}

export async function fetchProjets(
  filters: ProjetsFilters = {}
): Promise<PaginatedResponse<Projet>> {
  const params = new URLSearchParams()
  if (filters.categorie) params.set('categorie', String(filters.categorie))
  if (filters.difficulte) params.set('difficulte', filters.difficulte)
  if (filters.mis_en_avant) params.set('mis_en_avant', 'true')
  if (filters.search) params.set('search', filters.search)

  const query = params.toString()
  const url = `/projets/projets/${query ? `?${query}` : ''}`
  const response = await api.get<PaginatedResponse<Projet>>(url)
  return response.data
}

export async function fetchProjet(slug: string): Promise<Projet> {
  const response = await api.get<Projet>(`/projets/projets/${slug}/`)
  return response.data
}