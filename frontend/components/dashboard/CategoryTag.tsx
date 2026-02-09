'use client'

import { cn } from '@/lib/utils'
import { Briefcase, User, ShoppingCart, Heart, Tag } from 'lucide-react'

export type Category = 'work' | 'personal' | 'shopping' | 'health' | 'other'

export interface CategoryTagProps {
  category: Category
  size?: 'sm' | 'md' | 'lg'
  showIcon?: boolean
}

const categoryConfig = {
  work: {
    color: 'bg-category-work',
    text: 'Work',
    textColor: 'text-white',
    icon: Briefcase
  },
  personal: {
    color: 'bg-category-personal',
    text: 'Personal',
    textColor: 'text-white',
    icon: User
  },
  shopping: {
    color: 'bg-category-shopping',
    text: 'Shopping',
    textColor: 'text-white',
    icon: ShoppingCart
  },
  health: {
    color: 'bg-category-health',
    text: 'Health',
    textColor: 'text-white',
    icon: Heart
  },
  other: {
    color: 'bg-category-other',
    text: 'Other',
    textColor: 'text-white',
    icon: Tag
  }
}

const sizeConfig = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-3 py-1 text-sm',
  lg: 'px-4 py-1.5 text-base'
}

export function CategoryTag({
  category,
  size = 'md',
  showIcon = true
}: CategoryTagProps) {
  const config = categoryConfig[category]
  const Icon = config.icon

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1.5 rounded-md font-medium',
        config.color,
        config.textColor,
        sizeConfig[size]
      )}
      aria-label={`Category: ${config.text}`}
    >
      {showIcon && <Icon className="w-3.5 h-3.5" aria-hidden="true" />}
      {config.text}
    </span>
  )
}
