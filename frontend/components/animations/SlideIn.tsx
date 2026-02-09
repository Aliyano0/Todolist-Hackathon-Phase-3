'use client'

import { motion } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'

export type SlideDirection = 'up' | 'down' | 'left' | 'right'

export interface SlideInProps {
  children: React.ReactNode
  direction?: SlideDirection
  distance?: number
  delay?: number
  duration?: number
  className?: string
}

/**
 * SlideIn component wraps content with a slide-in animation from the specified direction.
 * Respects user's reduced motion preferences.
 *
 * Usage:
 * ```tsx
 * <SlideIn direction="up" distance={20} delay={0.1}>
 *   <YourContent />
 * </SlideIn>
 * ```
 */
export function SlideIn({
  children,
  direction = 'up',
  distance = 20,
  delay = 0,
  duration = 0.3,
  className = ''
}: SlideInProps) {
  const shouldReduceMotion = useReducedMotion()

  const getInitialPosition = () => {
    switch (direction) {
      case 'up':
        return { x: 0, y: distance }
      case 'down':
        return { x: 0, y: -distance }
      case 'left':
        return { x: distance, y: 0 }
      case 'right':
        return { x: -distance, y: 0 }
      default:
        return { x: 0, y: distance }
    }
  }

  const variants = shouldReduceMotion
    ? {
        hidden: { opacity: 1, x: 0, y: 0 },
        visible: { opacity: 1, x: 0, y: 0 }
      }
    : {
        hidden: {
          opacity: 0,
          ...getInitialPosition()
        },
        visible: {
          opacity: 1,
          x: 0,
          y: 0,
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
