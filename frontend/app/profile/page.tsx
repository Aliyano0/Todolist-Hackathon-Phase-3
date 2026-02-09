'use client';

import { useState, useEffect } from 'react';
import Navbar from '@/components/navigation/Navbar';
import { ThemeToggle } from '@/components/theme/ThemeToggle';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { useAuth } from '@/providers/AuthProvider';

export default function ProfilePage() {
  const { user } = useAuth();
  const [profile, setProfile] = useState({
    email: '',
    emailVerified: false,
    themePreference: 'system' as 'light' | 'dark' | 'system',
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load user profile data
    if (user) {
      setProfile({
        email: user.email,
        emailVerified: user.email_verified || false,
        themePreference: 'system',
      });
      setLoading(false);
    }
  }, [user]);

  const handleSave = () => {
    // In a real app, this would save to backend
    alert('Profile updated successfully!');
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-background flex items-center justify-center">
          <div className="text-lg">Loading profile...</div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-background">
        <Navbar />
        <main className="container mx-auto py-8 px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl mx-auto">
            <div className="mb-8">
              <h1 className="text-4xl font-bold text-foreground mb-2">Profile Settings</h1>
              <p className="text-lg text-muted-foreground">Manage your account and preferences</p>
            </div>

            <div className="rounded-xl border border-border bg-card text-card-foreground shadow-lg">
              <div className="flex flex-col space-y-1.5 p-6 border-b border-border">
                <h2 className="text-xl font-semibold leading-none tracking-tight text-foreground">Account Information</h2>
                <p className="text-sm text-muted-foreground">Manage your account settings and preferences</p>
              </div>
              <div className="p-6 space-y-6">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    Email Address
                  </label>
                  <input
                    type="email"
                    value={profile.email}
                    disabled
                    className="w-full px-3 py-2 border border-input rounded-lg bg-muted text-muted-foreground cursor-not-allowed"
                  />
                  <p className="text-xs text-muted-foreground mt-1.5">
                    Email cannot be changed
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-2">
                    Email Verification Status
                  </label>
                  <div className="flex items-center space-x-2">
                    <span className={`px-3 py-1.5 rounded-full text-xs font-medium ${profile.emailVerified ? 'bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300 border border-green-200 dark:border-green-800' : 'bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-300 border border-yellow-200 dark:border-yellow-800'}`}>
                      {profile.emailVerified ? '✓ Verified' : '⚠ Not Verified'}
                    </span>
                  </div>
                </div>

                <div className="pt-2">
                  <label className="block text-sm font-medium text-foreground mb-2">
                    Theme Preference
                  </label>
                  <div className="flex items-center space-x-4">
                    <select
                      value={profile.themePreference}
                      onChange={(e) => setProfile({...profile, themePreference: e.target.value as any})}
                      className="px-3 py-2 border border-input rounded-lg bg-background text-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-ring transition-colors"
                    >
                      <option value="system">System Default</option>
                      <option value="light">Light Mode</option>
                      <option value="dark">Dark Mode</option>
                    </select>
                    <ThemeToggle />
                  </div>
                  <p className="text-xs text-muted-foreground mt-1.5">
                    Choose your preferred color scheme
                  </p>
                </div>

                <div className="pt-4 border-t border-border">
                  <button
                    onClick={handleSave}
                    className="bg-primary text-primary-foreground py-2 px-6 rounded-lg hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 transition-all font-medium"
                  >
                    Save Changes
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </ProtectedRoute>
  );
}