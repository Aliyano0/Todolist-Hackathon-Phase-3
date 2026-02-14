'use client'

import Link from 'next/link'
import { ThemeToggle } from '@/components/theme/ThemeToggle'
import { useAuth } from '@/providers/AuthProvider'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'

export default function Navbar() {
  const { user, loading, signOut } = useAuth()
  const router = useRouter()

  const handleLogout = async () => {
    try {
      await signOut()
      router.push('/')
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  return (
    <nav className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
      <div className="container mx-auto px-4 py-3 flex justify-between items-center">
        <div className="flex items-center space-x-6">
          <Link href="/" className="text-xl font-bold text-foreground hover:text-primary transition-colors">
            AI Todo
          </Link>
          {user && (
            <div className="hidden md:flex items-center space-x-4">
              <Link
                href="/todos"
                className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
              >
                Dashboard
              </Link>
              <Link
                href="/chat"
                className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
              >
                AI Chat
              </Link>
              <Link
                href="/profile"
                className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors"
              >
                Profile
              </Link>
            </div>
          )}
        </div>

        <div className="flex items-center space-x-4">
          <ThemeToggle />
          {loading ? (
            <span className="text-sm text-muted-foreground">Loading...</span>
          ) : user ? (
            <div className="flex items-center space-x-3">
              <span className="hidden sm:inline text-sm text-muted-foreground">
                {user.email}
              </span>
              <Button
                onClick={handleLogout}
                variant="outline"
                size="sm"
                className="text-sm"
              >
                Logout
              </Button>
            </div>
          ) : (
            <div className="flex items-center space-x-2">
              <Button
                onClick={() => router.push('/login')}
                variant="ghost"
                size="sm"
                className="text-sm"
              >
                Login
              </Button>
              <Button
                onClick={() => router.push('/register')}
                size="sm"
                className="text-sm glowing-button"
              >
                Sign Up
              </Button>
            </div>
          )}
        </div>
      </div>
    </nav>
  )
}