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
        <main className="container mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl mx-auto">
            <h1 className="text-3xl font-bold text-foreground mb-8">Profile Settings</h1>

            <div className="rounded-xl border bg-card text-card-foreground shadow">
              <div className="flex flex-col space-y-1.5 p-6">
                <h2 className="font-semibold leading-none tracking-tight">Account Information</h2>
              </div>
              <div className="p-6 pt-0 space-y-4">
                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    Email
                  </label>
                  <input
                    type="email"
                    value={profile.email}
                    disabled
                    className="w-full px-3 py-2 border border-input rounded-md bg-muted cursor-not-allowed"
                  />
                  <p className="text-sm text-muted-foreground mt-1">
                    Email cannot be changed
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-foreground mb-1">
                    Email Verification Status
                  </label>
                  <div className="flex items-center space-x-2">
                    <span className={`px-3 py-1 rounded-full text-sm ${profile.emailVerified ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                      {profile.emailVerified ? 'Verified' : 'Not Verified'}
                    </span>
                  </div>
                </div>

                <div className="pt-4">
                  <label className="block text-sm font-medium text-foreground mb-1">
                    Theme Preference
                  </label>
                  <div className="flex items-center space-x-4">
                    <select
                      value={profile.themePreference}
                      onChange={(e) => setProfile({...profile, themePreference: e.target.value as any})}
                      className="px-3 py-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring"
                    >
                      <option value="system">System Default</option>
                      <option value="light">Light Mode</option>
                      <option value="dark">Dark Mode</option>
                    </select>
                    <ThemeToggle />
                  </div>
                </div>

                <div className="pt-4">
                  <button
                    onClick={handleSave}
                    className="bg-primary text-primary-foreground py-2 px-4 rounded-md hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
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