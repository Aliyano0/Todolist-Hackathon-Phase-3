'use client'

import { motion } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'
import { scaleInVariants } from '@/lib/animations'

export interface CTASectionProps {
  heading: string
  description: string
  buttonText: string
  onButtonClick: () => void
}

export function CTASection({
  heading,
  description,
  buttonText,
  onButtonClick
}: CTASectionProps) {
  const shouldReduceMotion = useReducedMotion()

  const variants = shouldReduceMotion
    ? { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { duration: 0 } } }
    : scaleInVariants

  return (
    <section className="py-20 px-4 bg-background">
      <motion.div
        className="max-w-3xl mx-auto text-center"
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "-100px" }}
        variants={variants}
      >
        <h2 className="text-4xl md:text-5xl font-bold mb-6 text-foreground">
          {heading}
        </h2>
        <p className="text-xl text-muted-foreground mb-8">
          {description}
        </p>
        <motion.button
          onClick={onButtonClick}
          className="glowing-button px-10 py-4 bg-primary text-primary-foreground rounded-lg font-semibold text-lg shadow-lg hover:shadow-xl transition-all"
          aria-label={buttonText}
          whileHover={{ scale: shouldReduceMotion ? 1 : 1.05 }}
          whileTap={{ scale: shouldReduceMotion ? 1 : 0.95 }}
          transition={{ duration: 0.15 }}
        >
          {buttonText}
        </motion.button>
      </motion.div>
    </section>
  )
}
