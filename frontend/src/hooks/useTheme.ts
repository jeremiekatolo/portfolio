import { useContext } from 'react'

import { ThemeContext } from '@/contexts/ThemeContext'

/**
 * Hook pour accéder au contexte de thème.
 * Doit être utilisé sous <ThemeProvider>.
 */
export function useTheme() {
  const ctx = useContext(ThemeContext)
  if (!ctx) {
    throw new Error('useTheme doit être utilisé dans un <ThemeProvider>')
  }
  return ctx
}