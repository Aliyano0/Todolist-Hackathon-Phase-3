'use client'

import { useState, useMemo } from 'react'
import { TaskList } from '@/components/dashboard/TaskList'
import { TaskForm } from '@/components/dashboard/TaskForm'
import { useTodos } from '@/hooks/useTodos'
import ProtectedRoute from '@/components/auth/ProtectedRoute'
import Navbar from '@/components/navigation/Navbar'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Plus, BarChart3, Search, Filter } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'

export default function TodosPage() {
  const { todos, loading, error, addTodo, updateTodo, deleteTodo, toggleComplete } = useTodos()
  const [showForm, setShowForm] = useState(false)
  const [editingTask, setEditingTask] = useState<any>(null)
  const [operatingTaskIds, setOperatingTaskIds] = useState<Set<string>>(new Set())
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Search and filter state
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState<'all' | 'completed' | 'pending'>('all')
  const [priorityFilter, setPriorityFilter] = useState<'all' | 'high' | 'medium' | 'low' | 'none'>('all')
  const [categoryFilter, setCategoryFilter] = useState<'all' | 'work' | 'personal' | 'shopping' | 'health' | 'other'>('all')
  const [sortBy, setSortBy] = useState<'date' | 'priority' | 'alphabetical'>('date')

  // Filter and sort tasks
  const filteredAndSortedTodos = useMemo(() => {
    let filtered = [...todos]

    // Search filter
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(task =>
        task.title.toLowerCase().includes(query) ||
        (task.description && task.description.toLowerCase().includes(query))
      )
    }

    // Status filter
    if (statusFilter !== 'all') {
      filtered = filtered.filter(task =>
        statusFilter === 'completed' ? task.completed : !task.completed
      )
    }

    // Priority filter
    if (priorityFilter !== 'all') {
      filtered = filtered.filter(task => task.priority === priorityFilter)
    }

    // Category filter
    if (categoryFilter !== 'all') {
      filtered = filtered.filter(task => task.category === categoryFilter)
    }

    // Sort
    filtered.sort((a, b) => {
      switch (sortBy) {
        case 'priority':
          const priorityOrder = { high: 0, medium: 1, low: 2, none: 3 }
          return priorityOrder[a.priority] - priorityOrder[b.priority]
        case 'alphabetical':
          return a.title.localeCompare(b.title)
        case 'date':
        default:
          // Sort by creation date (oldest first) to match chatbot task numbering
          return new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime()
      }
    })

    return filtered
  }, [todos, searchQuery, statusFilter, priorityFilter, categoryFilter, sortBy])

  const handleAddTodo = async (todoData: any) => {
    if (isSubmitting) return

    try {
      setIsSubmitting(true)
      await addTodo(todoData)
      setShowForm(false)
    } catch (err) {
      console.error('Error adding todo:', err)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleEditTodo = (taskId: string) => {
    const task = todos.find((t: any) => t.id === taskId)
    if (task) {
      setEditingTask(task)
      setShowForm(false) // Close create form if open
    }
  }

  const handleUpdateTodo = async (todoData: any) => {
    if (!editingTask || isSubmitting) return

    try {
      setIsSubmitting(true)
      await updateTodo(editingTask.id, todoData)
      setEditingTask(null)
    } catch (err) {
      console.error('Error updating todo:', err)
    } finally {
      setIsSubmitting(false)
    }
  }

  const handleCancelEdit = () => {
    setEditingTask(null)
  }

  const handleDeleteTodo = async (id: string) => {
    if (operatingTaskIds.has(id)) return

    try {
      setOperatingTaskIds(prev => new Set(prev).add(id))
      await deleteTodo(id)
    } catch (err) {
      console.error('Error deleting todo:', err)
    } finally {
      setOperatingTaskIds(prev => {
        const newSet = new Set(prev)
        newSet.delete(id)
        return newSet
      })
    }
  }

  const handleToggleComplete = async (id: string) => {
    if (operatingTaskIds.has(id)) return

    try {
      setOperatingTaskIds(prev => new Set(prev).add(id))
      await toggleComplete(id)
    } catch (err) {
      console.error('Error toggling todo:', err)
    } finally {
      setOperatingTaskIds(prev => {
        const newSet = new Set(prev)
        newSet.delete(id)
        return newSet
      })
    }
  }

  const stats = {
    total: todos.length,
    completed: todos.filter((t: any) => t.completed).length,
    pending: todos.filter((t: any) => !t.completed).length,
    highPriority: todos.filter((t: any) => t.priority === 'high' && !t.completed).length,
    filtered: filteredAndSortedTodos.length
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-background">
        <Navbar />
        <main className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-foreground mb-2">
              Task Dashboard
            </h1>
            <p className="text-lg text-muted-foreground">
              Manage your tasks with smart organization and priorities
            </p>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <Card>
              <CardHeader className="pb-2">
                <CardDescription>Total Tasks</CardDescription>
                <CardTitle className="text-3xl">{stats.total}</CardTitle>
              </CardHeader>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardDescription>Completed</CardDescription>
                <CardTitle className="text-3xl text-green-600">{stats.completed}</CardTitle>
              </CardHeader>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardDescription>Pending</CardDescription>
                <CardTitle className="text-3xl text-blue-600">{stats.pending}</CardTitle>
              </CardHeader>
            </Card>
            <Card>
              <CardHeader className="pb-2">
                <CardDescription>High Priority</CardDescription>
                <CardTitle className="text-3xl text-red-600">{stats.highPriority}</CardTitle>
              </CardHeader>
            </Card>
          </div>

          {/* Main Content */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Task List */}
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <CardTitle>Your Tasks</CardTitle>
                      <CardDescription>
                        {stats.filtered} of {stats.total} tasks
                      </CardDescription>
                    </div>
                    <Button
                      onClick={() => setShowForm(!showForm)}
                      size="sm"
                      className="glowing-button"
                    >
                      <Plus className="w-4 h-4 mr-2" />
                      New Task
                    </Button>
                  </div>

                  {/* Search and Filters */}
                  <div className="space-y-3">
                    {/* Search */}
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                      <Input
                        type="text"
                        placeholder="Search tasks..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="pl-10"
                      />
                    </div>

                    {/* Filters */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                      <Select value={statusFilter} onValueChange={(value: any) => setStatusFilter(value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="Status" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="all">All Status</SelectItem>
                          <SelectItem value="pending">Pending</SelectItem>
                          <SelectItem value="completed">Completed</SelectItem>
                        </SelectContent>
                      </Select>

                      <Select value={priorityFilter} onValueChange={(value: any) => setPriorityFilter(value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="Priority" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="all">All Priority</SelectItem>
                          <SelectItem value="high">High</SelectItem>
                          <SelectItem value="medium">Medium</SelectItem>
                          <SelectItem value="low">Low</SelectItem>
                          <SelectItem value="none">None</SelectItem>
                        </SelectContent>
                      </Select>

                      <Select value={categoryFilter} onValueChange={(value: any) => setCategoryFilter(value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="Category" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="all">All Categories</SelectItem>
                          <SelectItem value="work">Work</SelectItem>
                          <SelectItem value="personal">Personal</SelectItem>
                          <SelectItem value="shopping">Shopping</SelectItem>
                          <SelectItem value="health">Health</SelectItem>
                          <SelectItem value="other">Other</SelectItem>
                        </SelectContent>
                      </Select>

                      <Select value={sortBy} onValueChange={(value: any) => setSortBy(value)}>
                        <SelectTrigger>
                          <SelectValue placeholder="Sort by" />
                        </SelectTrigger>
                        <SelectContent>
                          <SelectItem value="date">Date Created</SelectItem>
                          <SelectItem value="priority">Priority</SelectItem>
                          <SelectItem value="alphabetical">Alphabetical</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <TaskList
                    tasks={filteredAndSortedTodos}
                    isLoading={loading}
                    error={error}
                    onComplete={handleToggleComplete}
                    onEdit={handleEditTodo}
                    onDelete={handleDeleteTodo}
                    operatingTaskIds={operatingTaskIds}
                  />
                </CardContent>
              </Card>
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              {/* Edit Task Form */}
              {editingTask && (
                <Card>
                  <CardHeader>
                    <CardTitle>Edit Task</CardTitle>
                    <CardDescription>
                      Update your task details
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <TaskForm
                      initialData={{
                        title: editingTask.title,
                        description: editingTask.description || '',
                        priority: editingTask.priority,
                        category: editingTask.category
                      }}
                      onSubmit={handleUpdateTodo}
                      onCancel={handleCancelEdit}
                      submitText="Update Task"
                      isSubmitting={isSubmitting}
                    />
                  </CardContent>
                </Card>
              )}

              {/* Task Form */}
              {showForm && !editingTask && (
                <Card>
                  <CardHeader>
                    <CardTitle>Create New Task</CardTitle>
                    <CardDescription>
                      Add a new task to your list
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <TaskForm
                      onSubmit={handleAddTodo}
                      onCancel={() => setShowForm(false)}
                      submitText="Create Task"
                      isSubmitting={isSubmitting}
                    />
                  </CardContent>
                </Card>
              )}

              {/* Productivity Insights */}
              <Card>
                <CardHeader>
                  <div className="flex items-center gap-2">
                    <BarChart3 className="w-5 h-5 text-primary" />
                    <CardTitle>Productivity Insights</CardTitle>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <div className="flex justify-between text-sm mb-1">
                      <span className="text-muted-foreground">Completion Rate</span>
                      <span className="font-medium">
                        {stats.total > 0 ? Math.round((stats.completed / stats.total) * 100) : 0}%
                      </span>
                    </div>
                    <div className="w-full bg-muted rounded-full h-2">
                      <div
                        className="bg-primary rounded-full h-2 transition-all"
                        style={{
                          width: `${stats.total > 0 ? (stats.completed / stats.total) * 100 : 0}%`
                        }}
                      />
                    </div>
                  </div>

                  <div className="pt-4 border-t border-border space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">Active Tasks</span>
                      <span className="font-medium">{stats.pending}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-muted-foreground">High Priority</span>
                      <span className="font-medium text-red-600">{stats.highPriority}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  )
}
