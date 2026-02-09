// Mock data for testing

export const mockTodos = [
  {
    id: '1',
    title: 'Learn Next.js',
    description: 'Go through the Next.js documentation',
    completed: false,
    priority: 'high',
    category: 'work',
    createdAt: new Date('2026-02-01'),
    updatedAt: new Date('2026-02-01')
  },
  {
    id: '2',
    title: 'Build Todo App',
    description: 'Create a beautiful todo application',
    completed: true,
    priority: 'medium',
    category: 'personal',
    createdAt: new Date('2026-02-01'),
    updatedAt: new Date('2026-02-01')
  },
  {
    id: '3',
    title: 'Buy groceries',
    description: 'Milk, eggs, bread, fruits',
    completed: false,
    priority: 'low',
    category: 'shopping',
    createdAt: new Date('2026-02-01'),
    updatedAt: new Date('2026-02-01')
  }
];

export const mockCategories = [
  {
    name: 'work',
    isCustom: false,
    createdAt: new Date('2026-02-01')
  },
  {
    name: 'personal',
    isCustom: false,
    createdAt: new Date('2026-02-01')
  },
  {
    name: 'shopping',
    isCustom: false,
    createdAt: new Date('2026-02-01')
  }
];