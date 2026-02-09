'use client'

import { useState } from 'react'
import { Priority } from './PriorityBadge'
import { Category } from './CategoryTag'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

export interface TaskFormData {
  title: string
  description: string
  priority: Priority
  category: Category
}

export interface TaskFormProps {
  initialData?: Partial<TaskFormData>
  onSubmit: (data: TaskFormData) => void
  onCancel: () => void
  submitText?: string
  isSubmitting?: boolean
}

export function TaskForm({
  initialData,
  onSubmit,
  onCancel,
  submitText = 'Create Task',
  isSubmitting = false
}: TaskFormProps) {
  const [formData, setFormData] = useState<TaskFormData>({
    title: initialData?.title || '',
    description: initialData?.description || '',
    priority: initialData?.priority || 'none',
    category: initialData?.category || 'other'
  })

  const [errors, setErrors] = useState<Partial<Record<keyof TaskFormData, string>>>({})

  const validateForm = (): boolean => {
    const newErrors: Partial<Record<keyof TaskFormData, string>> = {}

    if (!formData.title.trim()) {
      newErrors.title = 'Task title is required'
    } else if (formData.title.length > 200) {
      newErrors.title = 'Task title must be less than 200 characters'
    }

    if (formData.description.length > 1000) {
      newErrors.description = 'Description must be less than 1000 characters'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (validateForm()) {
      onSubmit(formData)
    }
  }

  const isValid = formData.title.trim().length > 0 && formData.title.length <= 200

  return (
    <form onSubmit={handleSubmit} className="space-y-4" aria-labelledby="task-form-heading">
      <h2 id="task-form-heading" className="sr-only">
        {initialData ? 'Edit Task' : 'Create New Task'}
      </h2>

      <div className="space-y-2">
        <Label htmlFor="title">
          Task Title <span className="text-destructive">*</span>
        </Label>
        <Input
          id="title"
          type="text"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          placeholder="Enter task title..."
          aria-required="true"
          aria-invalid={!!errors.title}
          aria-describedby={errors.title ? 'title-error' : undefined}
          disabled={isSubmitting}
        />
        {errors.title && (
          <p id="title-error" className="text-sm text-destructive" role="alert" aria-live="polite">
            {errors.title}
          </p>
        )}
      </div>

      <div className="space-y-2">
        <Label htmlFor="description">Description</Label>
        <Textarea
          id="description"
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          placeholder="Enter task description..."
          rows={3}
          aria-invalid={!!errors.description}
          aria-describedby={errors.description ? 'description-error' : undefined}
          disabled={isSubmitting}
        />
        {errors.description && (
          <p id="description-error" className="text-sm text-destructive" role="alert" aria-live="polite">
            {errors.description}
          </p>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <Label htmlFor="priority">
            Priority <span className="text-destructive">*</span>
          </Label>
          <Select
            value={formData.priority}
            onValueChange={(value) => setFormData({ ...formData, priority: value as Priority })}
            disabled={isSubmitting}
          >
            <SelectTrigger id="priority" aria-required="true">
              <SelectValue placeholder="Select priority" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="high">High</SelectItem>
              <SelectItem value="medium">Medium</SelectItem>
              <SelectItem value="low">Low</SelectItem>
              <SelectItem value="none">None</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="category">
            Category <span className="text-destructive">*</span>
          </Label>
          <Select
            value={formData.category}
            onValueChange={(value) => setFormData({ ...formData, category: value as Category })}
            disabled={isSubmitting}
          >
            <SelectTrigger id="category" aria-required="true">
              <SelectValue placeholder="Select category" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="work">Work</SelectItem>
              <SelectItem value="personal">Personal</SelectItem>
              <SelectItem value="shopping">Shopping</SelectItem>
              <SelectItem value="health">Health</SelectItem>
              <SelectItem value="other">Other</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <div className="flex gap-2 pt-2">
        <Button
          type="submit"
          disabled={!isValid || isSubmitting}
          className="flex-1"
          aria-disabled={!isValid || isSubmitting}
        >
          {isSubmitting ? 'Saving...' : submitText}
        </Button>
        <Button
          type="button"
          variant="outline"
          onClick={onCancel}
          disabled={isSubmitting}
        >
          Cancel
        </Button>
      </div>
    </form>
  )
}
