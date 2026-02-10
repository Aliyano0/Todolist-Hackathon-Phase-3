'use client'

import { motion } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'
import { ButtonHTMLAttributes, forwardRef } from 'react'

// Omit conflicting props between React and Framer Motion
type MotionButtonProps = Omit<
  ButtonHTMLAttributes<HTMLButtonElement>,
  'onDrag' | 'onDragStart' | 'onDragEnd' | 'onAnimationStart' | 'onAnimationEnd'
>

export interface AnimatedButtonProps extends MotionButtonProps {
  variant?: 'default' | 'glow'
  children: React.ReactNode
}

/**
 * AnimatedButton component wraps button content with hover and tap animations.
 * Respects user's reduced motion preferences.
 *
 * Usage:
 * ```tsx
 * <AnimatedButton variant="glow" onClick={handleClick}>
 *   Click Me
 * </AnimatedButton>
 * ```
 */
export const AnimatedButton = forwardRef<HTMLButtonElement, AnimatedButtonProps>(
  ({ variant = 'default', children, className = '', ...props }, ref) => {
    const shouldReduceMotion = useReducedMotion()

    const hoverScale = shouldReduceMotion ? 1 : 1.02
    const tapScale = shouldReduceMotion ? 1 : 0.98

    const baseClasses = variant === 'glow' ? 'button-glow' : ''

    return (
      <motion.button
        ref={ref}
        whileHover={{ scale: hoverScale }}
        whileTap={{ scale: tapScale }}
        transition={{ duration: 0.15, ease: 'easeInOut' }}
        className={`${baseClasses} ${className}`}
        {...props}
      >
        {children}
      </motion.button>
    )
  }
)

AnimatedButton.displayName = 'AnimatedButton'
