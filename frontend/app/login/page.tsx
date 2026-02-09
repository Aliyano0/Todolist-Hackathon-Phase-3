'use client';

import LoginForm from '@/components/auth/LoginForm';
import { useAuth } from '@/providers/AuthProvider';
import { useSearchParams } from 'next/navigation';
import { useEffect, useState, Suspense } from 'react';

function LoginContent() {
  const { loading } = useAuth();
  const searchParams = useSearchParams();
  const [message, setMessage] = useState('');

  useEffect(() => {
    const expired = searchParams.get('expired');
    if (expired === 'true') {
      setMessage('Your session has expired. Please log in again.');
    }
  }, [searchParams]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="text-lg text-muted-foreground">Loading...</div>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-background">
      <div className="w-full max-w-md px-4">
        {message && (
          <div className="mb-4 p-4 bg-yellow-50 dark:bg-yellow-900/30 border border-yellow-200 dark:border-yellow-700 rounded-lg">
            <p className="text-sm text-yellow-800 dark:text-yellow-200">{message}</p>
          </div>
        )}
        <LoginForm />
      </div>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="text-lg text-muted-foreground">Loading...</div>
      </div>
    }>
      <LoginContent />
    </Suspense>
  );
}
