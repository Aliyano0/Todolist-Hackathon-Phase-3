'use client';

import Navbar from '@/components/navigation/Navbar';
import { TodoList } from '@/components/todo/TodoList';
import { TodoForm } from '@/components/todo/TodoForm';
import { useTodos } from '@/hooks/useTodos';
import ProtectedRoute from '@/components/auth/ProtectedRoute';

export default function HomePage() {
  const { todos, loading, error, addTodo, updateTodo, deleteTodo, toggleComplete } = useTodos();

  const handleAddTodo = async (todoData: Omit<any, 'id' | 'createdAt' | 'updatedAt' | 'userId'>) => {
    await addTodo(todoData);
  };

  const handleUpdateTodo = async (id: string, updates: Partial<any>) => {
    await updateTodo(id, updates);
  };

  const handleDeleteTodo = async (id: string) => {
    await deleteTodo(id);
  };

  const handleToggleComplete = async (id: string) => {
    await toggleComplete(id);
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-background">
        <Navbar />
        <main className="container mx-auto py-6 px-4 sm:px-6 lg:px-8">
          {loading ? (
            <div className="container mx-auto py-6 px-4 sm:px-6 lg:px-8">
              <div className="animate-pulse">
                <div className="h-8 bg-muted rounded w-1/4 mb-6"></div>
                <div className="h-4 bg-muted rounded w-1/2 mb-4"></div>
              </div>
            </div>
          ) : error ? (
            <div className="container mx-auto py-6 px-4 sm:px-6 lg:px-8">
              <div className="rounded-lg bg-destructive/10 p-4 text-destructive">
                <h2 className="font-bold">Error Loading Todos</h2>
                <p className="mt-1">{error}</p>
              </div>
            </div>
          ) : (
            <>
              <div className="text-center mb-8">
                <h1 className="text-3xl font-bold text-foreground sm:text-4xl">
                  Todo Dashboard
                </h1>
                <p className="mt-2 text-sm text-muted-foreground">
                  Manage your tasks efficiently
                </p>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2">
                  <TodoList
                    todos={todos}
                    onUpdate={handleUpdateTodo}
                    onDelete={handleDeleteTodo}
                    onToggleComplete={handleToggleComplete}
                  />
                </div>
                <div>
                  <TodoForm onAddTodo={handleAddTodo} />

                  <div className="mt-6 p-4 bg-muted rounded-lg">
                    <h3 className="font-medium text-foreground">Statistics</h3>
                    <div className="mt-2 space-y-1 text-sm text-muted-foreground">
                      <p>Total todos: {todos.length}</p>
                      <p>Completed: {todos.filter((t: any) => t.completed).length}</p>
                      <p>Pending: {todos.filter((t: any) => !t.completed).length}</p>
                    </div>
                  </div>
                </div>
              </div>
            </>
          )}
        </main>
      </div>
    </ProtectedRoute>
  );
}