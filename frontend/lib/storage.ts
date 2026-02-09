// Local storage utility functions for the todo app

const STORAGE_KEY = 'todo-app-data';

export interface TodoAppData {
  todos: any[];
  categories: any[];
  // Add other data types as needed
}

export const loadFromStorage = (): TodoAppData => {
  try {
    const serializedData = localStorage.getItem(STORAGE_KEY);
    if (serializedData === null) {
      return { todos: [], categories: [] };
    }
    return JSON.parse(serializedData);
  } catch (error) {
    console.error('Error loading data from storage:', error);
    return { todos: [], categories: [] };
  }
};

export const saveToStorage = (data: TodoAppData): void => {
  try {
    const serializedData = JSON.stringify(data);
    localStorage.setItem(STORAGE_KEY, serializedData);
  } catch (error) {
    console.error('Error saving data to storage:', error);
  }
};

export const clearStorage = (): void => {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (error) {
    console.error('Error clearing storage:', error);
  }
};