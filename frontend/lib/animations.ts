// Animation Utilities for Framer Motion
// Feature: 020-frontend-ui-upgrade

import { Variants } from 'framer-motion'

// Animation variants for common patterns
export const fadeInVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { duration: 0.2, ease: [0.4, 0, 0.2, 1] }
  }
}

export const slideUpVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] }
  }
}

export const slideDownVariants: Variants = {
  hidden: { opacity: 0, y: -20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] }
  }
}

export const scaleInVariants: Variants = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.25, ease: [0.4, 0, 0.2, 1] }
  }
}

// Page transition variants
export const pageTransitionVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] }
  },
  exit: {
    opacity: 0,
    y: -20,
    transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] }
  }
}

// Stagger container for list animations
export const staggerContainerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
      delayChildren: 0.1
    }
  }
}

// Stagger item for list animations
export const staggerItemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.25 }
  }
}

// Spring configurations
export const springConfigs = {
  default: { stiffness: 300, damping: 30 },
  gentle: { stiffness: 200, damping: 25 },
  stiff: { stiffness: 400, damping: 35 }
}

// Animation durations (in seconds for Framer Motion)
export const durations = {
  fast: 0.15,
  normal: 0.2,
  medium: 0.25,
  slow: 0.3
}

// Easing functions
export const easings = {
  easeInOut: [0.4, 0, 0.2, 1] as const,
  easeOut: [0, 0, 0.2, 1] as const,
  easeIn: [0.4, 0, 1, 1] as const
}

// Helper function to create variants with reduced motion support
export function createVariants(
  shouldReduceMotion: boolean,
  normalVariants: Variants
): Variants {
  if (shouldReduceMotion) {
    return {
      hidden: { opacity: 0 },
      visible: { opacity: 1, transition: { duration: 0 } }
    }
  }
  return normalVariants
}
