'use client';

import Link from 'next/link';
import { ThemeToggle } from '@/components/theme/ThemeToggle';
import { useAuth } from '@/providers/AuthProvider';

export default function Navbar() {
  const { user, loading, signOut } = useAuth();

  const handleLogout = async () => {
    try {
      await signOut();
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  return (
    <nav className="border-b">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center space-x-4">
          <Link href="/" className="text-xl font-bold">
            Todo App
          </Link>
          <Link href="/todos" className="hover:underline">
            Todos
          </Link>
        </div>

        <div className="flex items-center space-x-4">
          <ThemeToggle />
          {loading ? (
            <span>Loading...</span>
          ) : user ? (
            <div className="flex items-center space-x-2">
              <span>Hello, {user.email}</span>
              <button
                onClick={handleLogout}
                className="hover:underline"
              >
                Logout
              </button>
            </div>
          ) : (
            <div className="flex space-x-2">
              <Link href="/login" className="hover:underline">
                Login
              </Link>
              <Link href="/register" className="hover:underline">
                Register
              </Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}