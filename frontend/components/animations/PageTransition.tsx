'use client'

import { motion, AnimatePresence } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'
import { pageTransitionVariants } from '@/lib/animations'

export interface PageTransitionProps {
  children: React.ReactNode
  className?: string
}

/**
 * PageTransition component wraps page content with smooth fade + slide animations
 * for route transitions. Respects user's reduced motion preferences.
 *
 * Usage:
 * ```tsx
 * <PageTransition>
 *   <YourPageContent />
 * </PageTransition>
 * ```
 */
export function PageTransition({ children, className = '' }: PageTransitionProps) {
  const shouldReduceMotion = useReducedMotion()

  const variants = shouldReduceMotion
    ? {
        initial: { opacity: 1 },
        animate: { opacity: 1 },
        exit: { opacity: 1 }
      }
    : pageTransitionVariants

  return (
    <AnimatePresence mode="wait">
      <motion.div
        initial="initial"
        animate="animate"
        exit="exit"
        variants={variants}
        className={className}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
