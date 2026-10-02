/**
 * Contexte de thème.
 *
 * Trois modes :
 * - 'clair'    : force le thème clair
 * - 'sombre'   : force le thème sombre
 * - 'systeme'  : suit la préférence de l'OS (par défaut)
 *
 * Le choix est persisté dans localStorage (clé `theme`).
 *
 * Le mode réel appliqué (clair ou sombre) est déterminé par :
 * - mode 'clair'   → 'clair'
 * - mode 'sombre'  → 'sombre'
 * - mode 'systeme' → préférence OS (via matchMedia)
 *
 * La classe `dark` est appliquée sur <html> quand le thème réel est sombre.
 */

import {
  createContext,
  useCallback,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'

export type ThemeMode = 'clair' | 'sombre' | 'systeme'
export type AppliedTheme = 'clair' | 'sombre'

interface ThemeContextValue {
  /** Mode choisi par l'utilisateur (peut être 'systeme'). */
  mode: ThemeMode
  /** Thème réellement appliqué ('clair' ou 'sombre'). */
  applied: AppliedTheme
  /** Change le mode. */
  setMode: (mode: ThemeMode) => void
}

export const ThemeContext = createContext<ThemeContextValue | null>(null)

const STORAGE_KEY = 'theme'

function lireModeStocke(): ThemeMode {
  if (typeof window === 'undefined') return 'systeme'
  const stocke = window.localStorage.getItem(STORAGE_KEY)
  if (stocke === 'clair' || stocke === 'sombre' || stocke === 'systeme') {
    return stocke
  }
  return 'systeme'
}

function lirePreferenceSysteme(): AppliedTheme {
  if (typeof window === 'undefined') return 'clair'
  return window.matchMedia('(prefers-color-scheme: dark)').matches
    ? 'sombre'
    : 'clair'
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [mode, setModeState] = useState<ThemeMode>(lireModeStocke)
  const [systemTheme, setSystemTheme] = useState<AppliedTheme>(lirePreferenceSysteme)

  // Écoute les changements de préférence OS en temps réel.
  useEffect(() => {
    const media = window.matchMedia('(prefers-color-scheme: dark)')
    const handleChange = (e: MediaQueryListEvent) => {
      setSystemTheme(e.matches ? 'sombre' : 'clair')
    }
    media.addEventListener('change', handleChange)
    return () => media.removeEventListener('change', handleChange)
  }, [])

  // Thème réellement appliqué selon le mode.
  const applied: AppliedTheme = useMemo(() => {
    if (mode === 'clair') return 'clair'
    if (mode === 'sombre') return 'sombre'
    return systemTheme
  }, [mode, systemTheme])

  // Applique la classe `dark` sur <html> et persiste le mode.
  useEffect(() => {
    const root = document.documentElement
    root.classList.toggle('dark', applied === 'sombre')
    window.localStorage.setItem(STORAGE_KEY, mode)
  }, [applied, mode])

  const setMode = useCallback((next: ThemeMode) => {
    setModeState(next)
  }, [])

  const value = useMemo(
    () => ({ mode, applied, setMode }),
    [mode, applied, setMode]
  )

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
}