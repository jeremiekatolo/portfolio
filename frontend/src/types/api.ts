/**
 * Types transverses pour l'API.
 *
 * Reproduit la structure de pagination DRF :
 *   {
 *     "count": 42,
 *     "next": "http://.../page=2",
 *     "previous": null,
 *     "results": [...]
 *   }
 */

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

/**
 * Erreur standard renvoyée par DRF :
 *   { "detail": "..." }  (erreur simple)
 *   { "champ": ["erreur 1", "erreur 2"] }  (erreur de validation)
 */
export interface ApiError {
  detail?: string
  [field: string]: string | string[] | undefined
}