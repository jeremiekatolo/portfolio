import { api } from './client'
import type { Article, PaginatedResponse } from '@/types'

export async function fetchArticles(): Promise<PaginatedResponse<Article>> {
  const response = await api.get<PaginatedResponse<Article>>(
    '/articles/articles/'
  )
  return response.data
}