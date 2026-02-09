'use client'

import { cn } from '@/lib/utils'

export type Priority = 'high' | 'medium' | 'low' | 'none'

export interface PriorityBadgeProps {
  priority: Priority
  size?: 'sm' | 'md' | 'lg'
  showIcon?: boolean
}

const priorityConfig = {
  high: {
    color: 'bg-priority-high',
    text: 'High',
    textColor: 'text-white'
  },
  medium: {
    color: 'bg-priority-medium',
    text: 'Medium',
    textColor: 'text-white'
  },
  low: {
    color: 'bg-priority-low',
    text: 'Low',
    textColor: 'text-white'
  },
  none: {
    color: 'bg-priority-none',
    text: 'None',
    textColor: 'text-white'
  }
}

const sizeConfig = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-3 py-1 text-sm',
  lg: 'px-4 py-1.5 text-base'
}

export function PriorityBadge({
  priority,
  size = 'md',
  showIcon = false
}: PriorityBadgeProps) {
  const config = priorityConfig[priority]

  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 rounded-full font-medium',
        config.color,
        config.textColor,
        sizeConfig[size]
      )}
      aria-label={`Priority: ${config.text}`}
    >
      {showIcon && <span className="w-1.5 h-1.5 rounded-full bg-current" aria-hidden="true" />}
      {config.text}
    </span>
  )
}
