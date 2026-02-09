'use client'

import { motion } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'
import { fadeInVariants } from '@/lib/animations'

export interface FadeInProps {
  children: React.ReactNode
  delay?: number
  duration?: number
  className?: string
}

/**
 * FadeIn component wraps content with a fade-in animation.
 * Respects user's reduced motion preferences.
 *
 * Usage:
 * ```tsx
 * <FadeIn delay={0.2} duration={0.3}>
 *   <YourContent />
 * </FadeIn>
 * ```
 */
export function FadeIn({
  children,
  delay = 0,
  duration = 0.3,
  className = ''
}: FadeInProps) {
  const shouldReduceMotion = useReducedMotion()

  const variants = shouldReduceMotion
    ? {
        hidden: { opacity: 1 },
        visible: { opacity: 1 }
      }
    : {
        hidden: { opacity: 0 },
        visible: {
          opacity: 1,
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
