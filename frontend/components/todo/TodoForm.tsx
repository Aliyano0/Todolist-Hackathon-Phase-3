'use client';

import { useState } from 'react';
import { TodoItem, PriorityLevel } from '@/lib/api';

interface TodoFormProps {
  onAddTodo: (todo: Omit<TodoItem, 'id' | 'createdAt' | 'updatedAt' | 'userId'>) => void;
}

export function TodoForm({ onAddTodo }: TodoFormProps) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<PriorityLevel>('medium');
  const [category, setCategory] = useState('personal');
  const [loading, setLoading] = useState(false);

  const predefinedCategories = ['work', 'personal', 'shopping'];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim() || loading) {
      return;
    }

    setLoading(true);
    try {
      await onAddTodo({
        title: title.trim(),
        description: description.trim() || undefined,
        completed: false,
        priority,
        category,
      });

      // Reset form
      setTitle('');
      setDescription('');
      setPriority('medium');
      setCategory('personal');
    } catch (error) {
      console.error('Error adding todo:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <label htmlFor="title" className="text-sm font-medium">
          Title *
        </label>
        <input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-3 py-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring disabled:opacity-50"
          placeholder="What needs to be done?"
          required
          disabled={loading}
        />
      </div>

      <div className="space-y-2">
        <label htmlFor="description" className="text-sm font-medium">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full px-3 py-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring disabled:opacity-50"
          placeholder="Additional details..."
          rows={3}
          disabled={loading}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-2">
          <label htmlFor="priority" className="text-sm font-medium">
            Priority
          </label>
          <select
            id="priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value as PriorityLevel)}
            className="w-full px-3 py-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring disabled:opacity-50"
            disabled={loading}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <div className="space-y-2">
          <label htmlFor="category" className="text-sm font-medium">
            Category
          </label>
          <select
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full px-3 py-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring disabled:opacity-50"
            disabled={loading}
          >
            {predefinedCategories.map((cat) => (
              <option key={cat} value={cat}>
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </option>
            ))}
            <option value="other">Other</option>
          </select>
        </div>
      </div>

      <button
        type="submit"
        className="w-full bg-primary text-primary-foreground py-2 px-4 rounded-md hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:opacity-50"
        disabled={loading}
      >
        {loading ? 'Adding...' : 'Add Todo'}
      </button>
    </form>
  );
}