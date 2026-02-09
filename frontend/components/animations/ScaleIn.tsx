'use client'

import { motion } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'

export interface ScaleInProps {
  children: React.ReactNode
  initialScale?: number
  delay?: number
  duration?: number
  className?: string
}

/**
 * ScaleIn component wraps content with a scale-in animation.
 * Respects user's reduced motion preferences.
 *
 * Usage:
 * ```tsx
 * <ScaleIn initialScale={0.95} delay={0.1}>
 *   <YourContent />
 * </ScaleIn>
 * ```
 */
export function ScaleIn({
  children,
  initialScale = 0.95,
  delay = 0,
  duration = 0.3,
  className = ''
}: ScaleInProps) {
  const shouldReduceMotion = useReducedMotion()

  const variants = shouldReduceMotion
    ? {
        hidden: { opacity: 1, scale: 1 },
        visible: { opacity: 1, scale: 1 }
      }
    : {
        hidden: {
          opacity: 0,
          scale: initialScale
        },
        visible: {
          opacity: 1,
          scale: 1,
          transition: {
            duration,
            delay,
            ease: [0.4, 0, 0.2, 1]
          }
        }
      }

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={variants}
      className={className}
    >
      {children}
    </motion.div>
  )
}
