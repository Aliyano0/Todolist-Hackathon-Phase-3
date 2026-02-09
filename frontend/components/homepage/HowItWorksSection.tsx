'use client'

import { motion } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'
import { staggerContainerVariants, staggerItemVariants } from '@/lib/animations'
import { ArrowRight } from 'lucide-react'

export interface Step {
  number: number
  title: string
  description: string
}

export interface HowItWorksSectionProps {
  steps: Step[]
  heading: string
}

export function HowItWorksSection({ steps, heading }: HowItWorksSectionProps) {
  const shouldReduceMotion = useReducedMotion()

  const containerVariants = shouldReduceMotion
    ? { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { duration: 0 } } }
    : staggerContainerVariants

  const itemVariants = shouldReduceMotion
    ? { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { duration: 0 } } }
    : staggerItemVariants

  return (
    <section className="py-20 px-4 bg-muted/30">
      <div className="max-w-6xl mx-auto">
        <motion.h2
          className="text-4xl md:text-5xl font-bold text-center mb-16 text-foreground"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={itemVariants}
        >
          {heading}
        </motion.h2>

        <motion.ol
          className="flex flex-col md:flex-row gap-8 md:gap-4 items-center justify-center"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={containerVariants}
        >
          {steps.map((step, index) => (
            <li key={step.number} className="flex items-center gap-4 flex-1">
              <motion.div
                className="flex flex-col items-center text-center max-w-xs"
                variants={itemVariants}
              >
                <div className="w-16 h-16 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-2xl font-bold mb-4">
                  {step.number}
                </div>
                <h3 className="text-xl font-semibold mb-2 text-foreground">
                  {step.title}
                </h3>
                <p className="text-muted-foreground">
                  {step.description}
                </p>
              </motion.div>

              {index < steps.length - 1 && (
                <ArrowRight
                  className="hidden md:block w-8 h-8 text-muted-foreground flex-shrink-0"
                  aria-hidden="true"
                />
              )}
            </li>
          ))}
        </motion.ol>
      </div>
    </section>
  )
}
