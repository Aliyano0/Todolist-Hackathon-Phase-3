import { useState } from 'react';

interface CategoryManagerProps {
  categories: string[];
  onAddCategory: (category: string) => void;
  onDeleteCategory: (category: string) => void;
}

export function CategoryManager({ categories, onAddCategory, onDeleteCategory }: CategoryManagerProps) {
  const [newCategory, setNewCategory] = useState('');

  const handleAddCategory = () => {
    if (newCategory.trim() && !categories.includes(newCategory.trim())) {
      onAddCategory(newCategory.trim());
      setNewCategory('');
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex space-x-2">
        <input
          type="text"
          value={newCategory}
          onChange={(e) => setNewCategory(e.target.value)}
          placeholder="New category name"
          className="flex-1 px-3 py-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring"
          onKeyPress={(e) => e.key === 'Enter' && handleAddCategory()}
        />
        <button
          onClick={handleAddCategory}
          className="px-4 py-2 bg-primary text-primary-foreground rounded-md hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring"
        >
          Add
        </button>
      </div>

      <div className="space-y-2">
        <h4 className="font-medium">Custom Categories:</h4>
        <div className="flex flex-wrap gap-2">
          {categories
            .filter(cat => !['work', 'personal', 'shopping'].includes(cat))
            .map((category) => (
              <div key={category} className="flex items-center bg-secondary px-3 py-1 rounded-full">
                <span className="mr-2">{category}</span>
                <button
                  onClick={() => onDeleteCategory(category)}
                  className="text-destructive hover:text-destructive/80"
                >
                  ×
                </button>
              </div>
            ))}
        </div>
      </div>
    </div>
  );
}