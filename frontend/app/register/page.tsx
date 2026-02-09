'use client';

import RegisterForm from '@/components/auth/RegisterForm';
import { useAuth } from '@/providers/AuthProvider';

export default function RegisterPage() {
  const { loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-background">
        <div className="text-lg text-muted-foreground">Loading...</div>
      </div>
    );
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-background py-12 px-4">
      <RegisterForm />
    </div>
  );
}