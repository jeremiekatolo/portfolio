import { api } from './client'
import type { Competence, PaginatedResponse } from '@/types'

export async function fetchCompetences(): Promise<PaginatedResponse<Competence>> {
  const response = await api.get<PaginatedResponse<Competence>>(
    '/competences/competences/'
  )
  return response.data
}