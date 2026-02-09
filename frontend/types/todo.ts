export type PriorityLevel = 'high' | 'medium' | 'low';

export interface TodoItem {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: PriorityLevel;
  category: string;
  createdAt: Date;
  updatedAt: Date;
}