import { useState, useEffect } from 'react';
import { TodoItem, apiClient } from '@/lib/api';
import { useAuth } from '@/providers/AuthProvider';

export function useTodos() {
  const [todos, setTodos] = useState<TodoItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const { user, isAuthenticated } = useAuth();

  // Load todos on mount and when user changes
  useEffect(() => {
    if (isAuthenticated && user) {
      fetchTodos();
    }
  }, [isAuthenticated, user]);

  // Listen for real-time task updates from chat widget
  useEffect(() => {
    const handleTaskUpdate = () => {
      if (isAuthenticated && user) {
        fetchTodos();
      }
    };

    window.addEventListener('taskUpdated', handleTaskUpdate);
    return () => window.removeEventListener('taskUpdated', handleTaskUpdate);
  }, [isAuthenticated, user]);

  const fetchTodos = async () => {
    if (!user) {
      setError('User not authenticated');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      const fetchedTodos = await apiClient.getTodos(user.id);
      setTodos(fetchedTodos);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch todos');
      console.error('Error fetching todos:', err);
    } finally {
      setLoading(false);
    }
  };

  const addTodo = async (todoData: Omit<TodoItem, 'id' | 'createdAt' | 'updatedAt' | 'userId'>) => {
    if (!user) {
      throw new Error('User not authenticated');
    }

    try {
      const newTodo = await apiClient.createTodo(user.id, todoData);
      setTodos(prev => [...prev, newTodo]);
      return newTodo;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add todo');
      console.error('Error adding todo:', err);
      throw err;
    }
  };

  const updateTodo = async (id: string, updates: Partial<TodoItem>) => {
    if (!user) {
      throw new Error('User not authenticated');
    }

    try {
      const updatedTodo = await apiClient.updateTodo(user.id, id, updates);
      setTodos(prev => prev.map(todo =>
        todo.id === id ? updatedTodo : todo
      ));
      return updatedTodo;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update todo');
      console.error('Error updating todo:', err);
      throw err;
    }
  };

  const deleteTodo = async (id: string) => {
    if (!user) {
      throw new Error('User not authenticated');
    }

    try {
      await apiClient.deleteTodo(user.id, id);
      setTodos(prev => prev.filter(todo => todo.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete todo');
      console.error('Error deleting todo:', err);
      throw err;
    }
  };

  const toggleTodoComplete = async (id: string) => {
    if (!user) {
      throw new Error('User not authenticated');
    }

    try {
      const updatedTodo = await apiClient.toggleTodoComplete(user.id, id);
      setTodos(prev => prev.map(todo =>
        todo.id === id ? updatedTodo : todo
      ));
      return updatedTodo;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to toggle todo completion');
      console.error('Error toggling todo completion:', err);
      throw err;
    }
  };

  return {
    todos,
    loading,
    error,
    fetchTodos,
    addTodo,
    updateTodo,
    deleteTodo,
    toggleComplete: toggleTodoComplete,
    setError
  };
}