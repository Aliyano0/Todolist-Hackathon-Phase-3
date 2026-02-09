'use client'

import { useState } from 'react'
import { TaskList } from '@/components/dashboard/TaskList'
import { TaskForm } from '@/components/dashboard/TaskForm'
import { useTodos } from '@/hooks/useTodos'
import ProtectedRoute from '@/components/auth/ProtectedRoute'
import Navbar from '@/components/navigation/Navbar'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Plus, BarChart3 } from 'lucide-react'
import { Button } from '@/components/ui/button'

export default function TodosPage() {
  const { todos, loading, error, addTodo, updateTodo, deleteTodo, toggleComplete } = useTodos()
  const [showForm, setShowForm] = useState(false)
  const [editingTask, setEditingTask] = useState<any>(null)

  const handleAddTodo = async (todoData: any) => {
    await addTodo(todoData)
    setShowForm(false)
  }

  const handleEditTodo = (taskId: string) => {
    const task = todos.find((t: any) => t.id === taskId)
    if (task) {
      setEditingTask(task)
      setShowForm(false) // Close create form if open
    }
  }

  const handleUpdateTodo = async (todoData: any) => {
    if (editingTask) {
      await updateTodo(editingTask.id, todoData)
      setEditingTask(null)
    }
  }

  const handleCancelEdit = () => {
    setEditingTask(null)
  }

  const handleDeleteTodo = async (id: string) => {
    await deleteTodo(id)
  }

  const handleToggleComplete = async (id: string) => {
    await toggleComplete(id)
  }

  const stats = {
    total: todos.length,
    completed: todos.filter((t: any) => t.completed).length,
    pending: todos.filter((t: any) => !t.completed).length,
    highPriority: todos.filter((t: any) => t.priority === 'high' && !t.completed).length
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
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle>Your Tasks</CardTitle>
                      <CardDescription>
                        {stats.pending} pending, {stats.completed} completed
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
                </CardHeader>
                <CardContent>
                  <TaskList
                    tasks={todos}
                    isLoading={loading}
                    error={error}
                    onComplete={handleToggleComplete}
                    onEdit={handleEditTodo}
                    onDelete={handleDeleteTodo}
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
