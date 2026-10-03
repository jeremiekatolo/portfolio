import { api } from './client'
import type { Categorie, PaginatedResponse } from '@/types'

export interface CategoriesFilters {
  type?: string
}

export async function fetchCategories(
  filters: CategoriesFilters = {}
): Promise<PaginatedResponse<Categorie>> {
  const params = new URLSearchParams()
  if (filters.type) params.set('type', filters.type)

  const query = params.toString()
  const url = `/categories/categories/${query ? `?${query}` : ''}`
  const response = await api.get<PaginatedResponse<Categorie>>(url)
  return response.data
}