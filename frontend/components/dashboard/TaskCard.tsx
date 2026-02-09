'use client'

import { motion } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'
import { scaleInVariants } from '@/lib/animations'
import { PriorityBadge, Priority } from './PriorityBadge'
import { CategoryTag, Category } from './CategoryTag'
import { Pencil, Trash2, Check, Clock } from 'lucide-react'
import { cn } from '@/lib/utils'

// Helper function to format date and time
function formatDateTime(dateString: string): string {
  // Parse the date string - handle both ISO format with/without timezone
  const date = new Date(dateString)

  // Check if date is valid
  if (isNaN(date.getTime())) {
    return 'Invalid date'
  }

  const now = new Date()
  const diffInMs = now.getTime() - date.getTime()
  const diffInMinutes = Math.floor(diffInMs / (1000 * 60))
  const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60))

  // If less than 1 minute ago
  if (diffInMinutes < 1) {
    return 'Just now'
  }

  // If less than 1 hour ago, show minutes
  if (diffInMinutes < 60) {
    if (diffInMinutes === 1) return '1 minute ago'
    return `${diffInMinutes} minutes ago`
  }

  // If less than 24 hours ago, show hours
  if (diffInHours < 24) {
    if (diffInHours === 1) return '1 hour ago'
    return `${diffInHours} hours ago`
  }

  // Otherwise show full date and time
  const options: Intl.DateTimeFormatOptions = {
    month: 'short',
    day: 'numeric',
    year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined,
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  }

  return date.toLocaleString('en-US', options)
}

export interface Task {
  id: string
  title: string
  description?: string
  priority: Priority
  category: Category
  completed: boolean
  createdAt: string
  updatedAt: string
}

export interface TaskCardProps {
  task: Task
  onComplete: (taskId: string) => void
  onEdit: (taskId: string) => void
  onDelete: (taskId: string) => void
  isEditing?: boolean
  isOperating?: boolean
}

const priorityBorderClass = {
  high: 'border-priority-high',
  medium: 'border-priority-medium',
  low: 'border-priority-low',
  none: 'border-priority-none'
}

const categoryTintClass = {
  work: 'bg-category-work-tint',
  personal: 'bg-category-personal-tint',
  shopping: 'bg-category-shopping-tint',
  health: 'bg-category-health-tint',
  other: 'bg-category-other-tint'
}

export function TaskCard({
  task,
  onComplete,
  onEdit,
  onDelete,
  isEditing = false,
  isOperating = false
}: TaskCardProps) {
  const shouldReduceMotion = useReducedMotion()

  const variants = shouldReduceMotion
    ? { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { duration: 0 } } }
    : scaleInVariants

  return (
    <motion.article
      className={cn(
        'group relative p-4 rounded-lg border-l-4 card-hover transition-all',
        priorityBorderClass[task.priority],
        categoryTintClass[task.category],
        task.completed && 'opacity-60'
      )}
      initial="hidden"
      animate="visible"
      variants={variants}
      role="article"
      aria-label={`Task: ${task.title}`}
    >
      <div className="flex items-start justify-between gap-4">
        <div className="flex items-start gap-3 flex-1">
          <button
            onClick={() => onComplete(task.id)}
            disabled={isOperating}
            className={cn(
              'mt-1 w-5 h-5 rounded border-2 flex items-center justify-center transition-colors',
              task.completed
                ? 'bg-primary border-primary text-primary-foreground'
                : 'border-muted-foreground hover:border-primary',
              isOperating && 'opacity-50 cursor-not-allowed'
            )}
            aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
          >
            {task.completed && <Check className="w-3 h-3" />}
          </button>

          <div className="flex-1">
            <h3
              className={cn(
                'text-lg font-semibold mb-1 text-foreground',
                task.completed && 'line-through'
              )}
            >
              {task.title}
            </h3>
            {task.description && (
              <p className="text-sm text-muted-foreground mb-2">
                {task.description}
              </p>
            )}
            <div className="flex items-center gap-2 mt-2 flex-wrap">
              <CategoryTag category={task.category} size="sm" />
              <div className="flex items-center gap-1 text-xs text-muted-foreground">
                <Clock className="w-3 h-3" />
                <span>{formatDateTime(task.createdAt)}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="flex flex-col items-end gap-2">
          <PriorityBadge priority={task.priority} size="sm" />

          <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <button
              onClick={() => onEdit(task.id)}
              disabled={isOperating}
              className={cn(
                'p-1.5 rounded hover:bg-muted transition-colors',
                isOperating && 'opacity-50 cursor-not-allowed'
              )}
              aria-label={`Edit task: ${task.title}`}
            >
              <Pencil className="w-4 h-4 text-muted-foreground" />
            </button>
            <button
              onClick={() => onDelete(task.id)}
              disabled={isOperating}
              className={cn(
                'p-1.5 rounded hover:bg-destructive/10 transition-colors',
                isOperating && 'opacity-50 cursor-not-allowed'
              )}
              aria-label={`Delete task: ${task.title}`}
            >
              <Trash2 className="w-4 h-4 text-destructive" />
            </button>
          </div>
        </div>
      </div>
    </motion.article>
  )
}
