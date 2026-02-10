'use client';

import { useState, useMemo } from 'react';
import { TodoItem } from './TodoItem';
import { TodoItem as TodoItemType, PriorityLevel } from '@/lib/api';

interface TodoListProps {
  todos: TodoItemType[];
  onUpdate: (id: string, updates: Partial<TodoItemType>) => Promise<void>;
  onDelete: (id: string) => void;
  onToggleComplete: (id: string) => void;
}

export function TodoList({ todos, onUpdate, onDelete, onToggleComplete }: TodoListProps) {
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [sortBy, setSortBy] = useState<'priority' | 'category' | 'date'>('date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedPriority, setSelectedPriority] = useState<PriorityLevel | 'all'>('all');

  // Get unique categories for filter dropdown
  const uniqueCategories = useMemo(() => {
    const categories = new Set(todos.map(todo => todo.category));
    return Array.from(categories).sort();
  }, [todos]);

  // Filter and sort todos
  const filteredAndSortedTodos = useMemo(() => {
    let result = [...todos];

    // Apply filters
    if (filter === 'active') {
      result = result.filter(todo => !todo.completed);
    } else if (filter === 'completed') {
      result = result.filter(todo => todo.completed);
    }

    if (selectedCategory !== 'all') {
      result = result.filter(todo => todo.category === selectedCategory);
    }

    if (selectedPriority !== 'all') {
      result = result.filter(todo => todo.priority === selectedPriority);
    }

    // Apply sorting
    result.sort((a, b) => {
      let comparison = 0;

      if (sortBy === 'priority') {
        const priorityOrder: Record<PriorityLevel, number> = { high: 3, medium: 2, low: 1, none: 0 };
        comparison = priorityOrder[b.priority] - priorityOrder[a.priority]; // High priority first
      } else if (sortBy === 'category') {
        comparison = a.category.localeCompare(b.category);
      } else { // sortBy === 'date'
        comparison = new Date(a.createdAt).getTime() - new Date(b.createdAt).getTime();
      }

      return sortOrder === 'asc' ? comparison : -comparison;
    });

    return result;
  }, [todos, filter, sortBy, sortOrder, selectedCategory, selectedPriority]);

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <h2 className="text-xl font-semibold">Your Tasks</h2>

        <div className="flex flex-wrap gap-2">
          {/* Filter by completion status */}
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value as 'all' | 'active' | 'completed')}
            className="px-3 py-1 border border-input rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="all">All Tasks</option>
            <option value="active">Active</option>
            <option value="completed">Completed</option>
          </select>

          {/* Filter by category */}
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-3 py-1 border border-input rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="all">All Categories</option>
            {uniqueCategories.map(category => (
              <option key={category} value={category}>
                {category}
              </option>
            ))}
          </select>

          {/* Filter by priority */}
          <select
            value={selectedPriority}
            onChange={(e) => setSelectedPriority(e.target.value as PriorityLevel | 'all')}
            className="px-3 py-1 border border-input rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="all">All Priorities</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>

          {/* Sort by */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as 'priority' | 'category' | 'date')}
            className="px-3 py-1 border border-input rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          >
            <option value="date">Sort by Date</option>
            <option value="priority">Sort by Priority</option>
            <option value="category">Sort by Category</option>
          </select>

          {/* Sort order */}
          <button
            onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
            className="px-3 py-1 border border-input rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-ring"
          >
            {sortOrder === 'asc' ? '↑' : '↓'}
          </button>
        </div>
      </div>

      {filteredAndSortedTodos.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">
          <p>No todos match the current filters.</p>
        </div>
      ) : (
        <ul className="space-y-2">
          {filteredAndSortedTodos.map((todo) => (
            <TodoItem
              key={todo.id}
              todo={todo}
              onUpdate={onUpdate}
              onDelete={onDelete}
              onToggleComplete={onToggleComplete}
            />
          ))}
        </ul>
      )}
    </div>
  );
}