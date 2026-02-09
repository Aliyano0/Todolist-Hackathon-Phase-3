// Hook to detect user's reduced motion preference
// Feature: 020-frontend-ui-upgrade

'use client'

import { useEffect, useState } from 'react'

export function useReducedMotion(): boolean {
  const [shouldReduceMotion, setShouldReduceMotion] = useState(false)

  useEffect(() => {
    // Check if window is available (client-side only)
    if (typeof window === 'undefined') {
      return
    }

    // Create media query to detect reduced motion preference
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)')

    // Set initial value
    setShouldReduceMotion(mediaQuery.matches)

    // Listen for changes to the preference
    const listener = (event: MediaQueryListEvent) => {
      setShouldReduceMotion(event.matches)
    }

    // Add event listener
    mediaQuery.addEventListener('change', listener)

    // Cleanup
    return () => {
      mediaQuery.removeEventListener('change', listener)
    }
  }, [])

  return shouldReduceMotion
}
