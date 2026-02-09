'use client';

import { useState } from 'react';
import { TodoActions } from './TodoActions';
import { TodoItem as TodoItemType } from '@/lib/api';

interface TodoItemProps {
  todo: TodoItemType;
  onUpdate: (id: string, updates: Partial<TodoItemType>) => Promise<void>;
  onDelete: (id: string) => void;
  onToggleComplete: (id: string) => void;
}

export function TodoItem({ todo, onUpdate, onDelete, onToggleComplete }: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');
  const [loading, setLoading] = useState(false);

  const handleToggleComplete = () => {
    if (loading) return;
    onToggleComplete(todo.id);
  };

  const handleDelete = () => {
    if (loading) return;
    onDelete(todo.id);
  };

  const handleSaveEdit = () => {
    if (loading) return;

    setLoading(true);
    onUpdate(todo.id, {
      title: editTitle,
      description: editDescription,
    })
    .then(() => {
      setIsEditing(false);
    })
    .finally(() => {
      setLoading(false);
    });
  };

  const handleCancelEdit = () => {
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setIsEditing(false);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      handleCancelEdit();
    }
  };

  return (
    <li className="flex items-center justify-between p-3 border rounded-lg bg-card">
      {isEditing ? (
        <div className="flex-grow space-y-2">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="w-full px-2 py-1 border rounded focus:outline-none focus:ring-1 focus:ring-primary"
            onKeyDown={handleKeyDown}
            autoFocus
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="w-full px-2 py-1 border rounded focus:outline-none focus:ring-1 focus:ring-primary"
            rows={2}
            onKeyDown={handleKeyDown}
          />
          <div className="flex space-x-2 mt-1">
            <button
              onClick={handleSaveEdit}
              disabled={loading}
              className="text-xs bg-primary text-primary-foreground px-2 py-1 rounded hover:bg-primary/90 disabled:opacity-50"
            >
              {loading ? 'Saving...' : 'Save'}
            </button>
            <button
              onClick={handleCancelEdit}
              disabled={loading}
              className="text-xs bg-secondary text-secondary-foreground px-2 py-1 rounded hover:bg-secondary/80 disabled:opacity-50"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="flex items-center space-x-3 flex-1">
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={handleToggleComplete}
            className="h-4 w-4 rounded border-input text-primary focus:ring-primary disabled:opacity-50"
            disabled={loading}
          />
          <div className="flex-1">
            <div className="flex items-center justify-between">
              <h3 className={`font-medium ${todo.completed ? 'line-through text-muted-foreground' : 'text-foreground'}`}>
                {todo.title}
              </h3>
              <span className={`ml-2 text-xs px-2 py-1 rounded-full ${
                todo.priority === 'high' ? 'bg-red-100 text-red-800' :
                todo.priority === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-green-100 text-green-800'
              }`}>
                {todo.priority}
              </span>
            </div>
            {todo.description && (
              <p className="text-sm text-muted-foreground mt-1">
                {todo.description}
              </p>
            )}
            <div className="mt-1">
              <span className="inline-block text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
                {todo.category}
              </span>
            </div>
          </div>
        </div>
      )}
      {!isEditing && (
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setIsEditing(true)}
            disabled={loading}
            className="text-xs text-primary hover:text-primary/80 disabled:opacity-50"
          >
            Edit
          </button>
          <TodoActions
            completed={todo.completed}
            onToggleComplete={handleToggleComplete}
            onDelete={handleDelete}
          />
        </div>
      )}
    </li>
  );
}