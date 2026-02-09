'use client'

import { usePathname } from 'next/navigation'
import { AnimatePresence, motion } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'
import { pageTransitionVariants } from '@/lib/animations'

/**
 * PageTransitionWrapper provides smooth page transitions for Next.js App Router.
 * This component wraps the children and animates on route changes.
 */
export function PageTransitionWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const shouldReduceMotion = useReducedMotion()

  const variants = shouldReduceMotion
    ? {
        initial: { opacity: 1 },
        animate: { opacity: 1 },
        exit: { opacity: 1 }
      }
    : pageTransitionVariants

  return (
    <AnimatePresence mode="wait" initial={false}>
      <motion.div
        key={pathname}
        initial="initial"
        animate="animate"
        exit="exit"
        variants={variants}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
