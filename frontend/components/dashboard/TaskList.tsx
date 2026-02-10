'use client'

import { motion } from 'framer-motion'
import { useReducedMotion } from '@/hooks/useReducedMotion'
import { staggerContainerVariants, staggerItemVariants } from '@/lib/animations'
import { TaskCard, Task } from './TaskCard'
import { Loader2, AlertCircle, Inbox } from 'lucide-react'

export interface TaskListProps {
  tasks: Task[]
  isLoading: boolean
  error?: string | null
  onComplete: (taskId: string) => void
  onEdit: (taskId: string) => void
  onDelete: (taskId: string) => void
  operatingTaskIds?: Set<string>
  emptyMessage?: string
}

export function TaskList({
  tasks,
  isLoading,
  error,
  onComplete,
  onEdit,
  onDelete,
  operatingTaskIds = new Set(),
  emptyMessage = 'No tasks yet. Create your first task to get started!'
}: TaskListProps) {
  const shouldReduceMotion = useReducedMotion()

  const containerVariants = shouldReduceMotion
    ? { hidden: { opacity: 0 }, visible: { opacity: 1, transition: { duration: 0 } } }
    : staggerContainerVariants

  if (isLoading) {
    return (
      <div
        className="flex items-center justify-center py-12"
        aria-live="polite"
        aria-busy="true"
      >
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
        <span className="sr-only">Loading tasks...</span>
      </div>
    )
  }

  if (error) {
    return (
      <div
        className="rounded-lg bg-destructive/10 p-6 text-destructive"
        role="alert"
      >
        <div className="flex items-center gap-2 mb-2">
          <AlertCircle className="w-5 h-5" />
          <h3 className="font-semibold">Error Loading Tasks</h3>
        </div>
        <p className="text-sm">{error}</p>
      </div>
    )
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-12">
        <Inbox className="w-16 h-16 mx-auto mb-4 text-muted-foreground" />
        <p className="text-lg text-muted-foreground">{emptyMessage}</p>
      </div>
    )
  }

  return (
    <motion.ul
      className="space-y-4"
      initial="hidden"
      animate="visible"
      variants={containerVariants}
    >
      {tasks.map((task) => (
        <motion.li key={task.id} variants={staggerItemVariants}>
          <TaskCard
            task={task}
            onComplete={onComplete}
            onEdit={onEdit}
            onDelete={onDelete}
            isOperating={operatingTaskIds.has(task.id)}
          />
        </motion.li>
      ))}
    </motion.ul>
  )
}
