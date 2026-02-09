'use client'

import { motion } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'
import { fadeInVariants, slideUpVariants } from '@/lib/animations'
import { useRouter } from 'next/navigation'

export interface HeroSectionProps {
  title: string
  subtitle: string
  primaryCTA: string
  secondaryCTA: string
  onPrimaryCTAClick: () => void
  onSecondaryCTAClick: () => void
  isAuthenticated: boolean
}

export function HeroSection({
  title,
  subtitle,
  primaryCTA,
  secondaryCTA,
  onPrimaryCTAClick,
  onSecondaryCTAClick,
  isAuthenticated
}: HeroSectionProps) {
  const shouldReduceMotion = useReducedMotion()
  const router = useRouter()

  const variants = shouldReduceMotion
    ? { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { duration: 0 } } }
    : slideUpVariants

  return (
    <motion.section
      className="min-h-screen flex items-center justify-center hero-gradient px-4 py-20"
      initial="hidden"
      animate="visible"
      variants={variants}
    >
      <div className="max-w-4xl mx-auto text-center text-white">
        <motion.h1
          className="text-5xl md:text-6xl lg:text-7xl font-bold mb-6"
          variants={variants}
        >
          {title}
        </motion.h1>

        <motion.p
          className="text-xl md:text-2xl mb-12 text-white/90"
          variants={variants}
        >
          {subtitle}
        </motion.p>

        <motion.div
          className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          variants={variants}
        >
          {isAuthenticated ? (
            <>
              <motion.button
                onClick={() => router.push('/todos')}
                className="glowing-button px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transition-all"
                aria-label="Go to Dashboard"
                whileHover={{ scale: shouldReduceMotion ? 1 : 1.05 }}
                whileTap={{ scale: shouldReduceMotion ? 1 : 0.95 }}
                transition={{ duration: 0.15 }}
              >
                Dashboard
              </motion.button>
              <motion.button
                onClick={() => router.push('/profile')}
                className="px-8 py-4 border-2 border-white text-white rounded-lg font-semibold text-lg hover:bg-white hover:text-blue-600 transition-all"
                aria-label="Go to Profile"
                whileHover={{ scale: shouldReduceMotion ? 1 : 1.05 }}
                whileTap={{ scale: shouldReduceMotion ? 1 : 0.95 }}
                transition={{ duration: 0.15 }}
              >
                Profile
              </motion.button>
            </>
          ) : (
            <>
              <motion.button
                onClick={onPrimaryCTAClick}
                className="glowing-button px-8 py-4 bg-white text-blue-600 rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transition-all"
                aria-label={primaryCTA}
                whileHover={{ scale: shouldReduceMotion ? 1 : 1.05 }}
                whileTap={{ scale: shouldReduceMotion ? 1 : 0.95 }}
                transition={{ duration: 0.15 }}
              >
                {primaryCTA}
              </motion.button>
              <motion.button
                onClick={onSecondaryCTAClick}
                className="px-8 py-4 border-2 border-white text-white rounded-lg font-semibold text-lg hover:bg-white hover:text-blue-600 transition-all"
                aria-label={secondaryCTA}
                whileHover={{ scale: shouldReduceMotion ? 1 : 1.05 }}
                whileTap={{ scale: shouldReduceMotion ? 1 : 0.95 }}
                transition={{ duration: 0.15 }}
              >
                {secondaryCTA}
              </motion.button>
            </>
          )}
        </motion.div>
      </div>
    </motion.section>
  )
}
