'use client';

import React, { useState, useEffect, useContext } from 'react';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const toastVariants = cva(
  'fixed top-4 right-4 z-50 w-full max-w-sm overflow-hidden rounded-md shadow-lg transition-all data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-80 data-[state=open]:slide-in-from-top-full data-[state=open]:sm:slide-in-from-bottom-full',
  {
    variants: {
      variant: {
        default: 'bg-background border',
        destructive:
          'destructive group border-destructive bg-destructive text-destructive-foreground',
      },
      position: {
        topRight: 'top-4 right-4',
        bottomRight: 'bottom-4 right-4',
        topLeft: 'top-4 left-4',
        bottomLeft: 'bottom-4 left-4',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
);

interface ToastProps extends VariantProps<typeof toastVariants> {
  title?: string;
  description?: string;
  duration?: number;
  onClose?: () => void;
  position?: 'topRight' | 'bottomRight' | 'topLeft' | 'bottomLeft';
}

export function Toast({
  title,
  description,
  variant,
  duration = 5000,
  onClose,
  position = 'topRight',
}: ToastProps) {
  const [open, setOpen] = useState(true);

  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        setOpen(false);
        onClose?.();
      }, duration);

      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);

  if (!open) return null;

  return (
    <div
      className={cn(toastVariants({ variant, position }))}
      role="status"
      aria-live="polite"
      aria-atomic="true"
    >
      <div className="pointer-events-auto w-full max-w-sm overflow-hidden rounded-md shadow-lg ring-1 ring-black ring-opacity-5">
        <div className="p-4">
          <div className="flex items-start">
            <div className="ml-3 w-0 flex-1 pt-0.5">
              {title && (
                <p className="text-sm font-medium text-foreground">
                  {title}
                </p>
              )}
              {description && (
                <p className="mt-1 text-sm text-muted-foreground">
                  {description}
                </p>
              )}
            </div>
            <div className="ml-4 flex flex-shrink-0">
              <button
                type="button"
                className="inline-flex rounded-md text-foreground hover:text-foreground/80 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
                onClick={() => {
                  setOpen(false);
                  onClose?.();
                }}
              >
                <span className="sr-only">Close</span>
                <svg
                  className="h-5 w-5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Toast Provider to manage multiple toasts
interface ToastContextType {
  addToast: (toast: Omit<ToastProps, 'onClose'>) => void;
}

const ToastContext = React.createContext<ToastContextType | undefined>(undefined);

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Array<Omit<ToastProps, 'onClose'> & { id: string }>>([]);

  const addToast = (toast: Omit<ToastProps, 'onClose'>) => {
    const id = Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev, { ...toast, id }]);
  };

  const removeToast = (id: string) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  };

  return (
    <ToastContext.Provider value={{ addToast }}>
      {children}
      {toasts.map(({ id, ...toastProps }) => (
        <Toast
          key={id}
          {...toastProps}
          onClose={() => removeToast(id)}
        />
      ))}
    </ToastContext.Provider>
  );
}

export const useToast = () => {
  const context = useContext(ToastContext);
  if (context === undefined) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
};