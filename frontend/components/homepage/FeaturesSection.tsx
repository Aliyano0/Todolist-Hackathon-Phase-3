'use client'

import { motion } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'
import { staggerContainerVariants, staggerItemVariants } from '@/lib/animations'
import { Sparkles, Tags, RefreshCw, BarChart3 } from 'lucide-react'

export interface Feature {
  id: string
  title: string
  description: string
  icon: string
}

export interface FeaturesSectionProps {
  features: Feature[]
  heading: string
  subheading?: string
}

const iconMap = {
  sparkles: Sparkles,
  tags: Tags,
  refresh: RefreshCw,
  chart: BarChart3
}

export function FeaturesSection({
  features,
  heading,
  subheading
}: FeaturesSectionProps) {
  const shouldReduceMotion = useReducedMotion()

  const containerVariants = shouldReduceMotion
    ? { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { duration: 0 } } }
    : staggerContainerVariants

  const itemVariants = shouldReduceMotion
    ? { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { duration: 0 } } }
    : staggerItemVariants

  return (
    <section className="py-20 px-4 bg-background" aria-labelledby="features-heading">
      <div className="max-w-6xl mx-auto">
        <motion.div
          className="text-center mb-16"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={itemVariants}
        >
          <h2 id="features-heading" className="text-4xl md:text-5xl font-bold mb-4 text-foreground">
            {heading}
          </h2>
          {subheading && (
            <p className="text-xl text-muted-foreground">{subheading}</p>
          )}
        </motion.div>

        <motion.div
          className="grid grid-cols-1 md:grid-cols-2 gap-8"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-100px" }}
          variants={containerVariants}
        >
          {features.map((feature) => {
            const IconComponent = iconMap[feature.icon as keyof typeof iconMap] || Sparkles

            return (
              <motion.article
                key={feature.id}
                className="p-8 rounded-lg bg-card border border-border hover:border-primary/50 transition-colors"
                variants={itemVariants}
              >
                <div className="flex items-start gap-4">
                  <div className="p-3 rounded-lg bg-primary/10 text-primary">
                    <IconComponent className="w-6 h-6" aria-hidden="true" />
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold mb-2 text-card-foreground">
                      {feature.title}
                    </h3>
                    <p className="text-muted-foreground">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </motion.article>
            )
          })}
        </motion.div>
      </div>
    </section>
  )
}
