import { api } from './client'
import type { Article, PaginatedResponse } from '@/types'

export interface ArticlesFilters {
  categorie?: number
  search?: string
}

export async function fetchArticles(
  filters: ArticlesFilters = {}
): Promise<PaginatedResponse<Article>> {
  const params = new URLSearchParams()
  if (filters.categorie) params.set('categorie', String(filters.categorie))
  if (filters.search) params.set('search', filters.search)

  const query = params.toString()
  const url = `/articles/articles/${query ? `?${query}` : ''}`
  const response = await api.get<PaginatedResponse<Article>>(url)
  return response.data
}

export async function fetchArticle(slug: string): Promise<Article> {
  const response = await api.get<Article>(`/articles/articles/${slug}/`)
  return response.data
}