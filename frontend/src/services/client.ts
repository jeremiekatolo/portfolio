/**
 * Client HTTP central.
 *
 * - Base URL lue depuis VITE_API_BASE_URL (fallback localhost:8000).
 * - Cookie de session envoyé automatiquement (withCredentials).
 * - CSRF : lit le cookie `csrftoken` et l'envoie dans l'en-tête
 *   X-CSRFToken pour les requêtes non-safe (POST, PUT, PATCH, DELETE).
 * - Gestion centralisée des erreurs (401, 403, 404, 500).
 */

import axios, { AxiosError, type AxiosInstance } from 'axios'

const baseURL = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'

/**
 * Lit un cookie par son nom.
 * Utilisé pour récupérer le token CSRF.
 */
function getCookie(name: string): string | null {
  const match = document.cookie.match(
    new RegExp('(^|;\\s*)' + name + '=([^;]*)')
  )
  return match ? decodeURIComponent(match[2]) : null
}

export const api: AxiosInstance = axios.create({
  baseURL,
  withCredentials: true, // envoie les cookies de session Django
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
  timeout: 15000,
})

/**
 * Intercepteur de requête : ajoute le CSRF token aux requêtes mutatives.
 */
api.interceptors.request.use((config) => {
  const method = (config.method ?? 'get').toLowerCase()
  if (['post', 'put', 'patch', 'delete'].includes(method)) {
    const csrf = getCookie('csrftoken')
    if (csrf) {
      config.headers = config.headers ?? {}
      config.headers['X-CSRFToken'] = csrf
    }
  }
  return config
})

/**
 * Intercepteur de réponse : normalise les erreurs.
 */
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // On peut brancher plus tard un toast/notification ici.
    if (error.response) {
      const status = error.response.status
      if (status === 401) {
        // Non authentifié
      } else if (status === 403) {
        // Permission refusée
      } else if (status === 404) {
        // Ressource inexistante
      }
    }
    return Promise.reject(error)
  }
)