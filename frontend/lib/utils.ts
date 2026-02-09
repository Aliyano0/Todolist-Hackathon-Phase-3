import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Utility functions for theme management
export const themeUtils = {
  getSystemTheme: (): 'light' | 'dark' => {
    if (typeof window !== 'undefined') {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
    return 'light';
  },

  isValidTheme: (theme: string): theme is 'light' | 'dark' => {
    return theme === 'light' || theme === 'dark';
  }
};

// Utility functions for date formatting
export const dateUtils = {
  formatDateTime: (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString();
  },

  formatDate: (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString();
  },

  formatTime: (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleTimeString();
  }
};

// Utility functions for string manipulation
export const stringUtils = {
  truncate: (str: string, maxLength: number): string => {
    if (str.length <= maxLength) return str;
    return str.substring(0, maxLength) + '...';
  },

  capitalize: (str: string): string => {
    if (!str) return str;
    return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
  }
};