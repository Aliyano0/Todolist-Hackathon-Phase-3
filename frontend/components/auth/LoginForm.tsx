'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/providers/AuthProvider';

interface ValidationErrors {
  email?: string;
  password?: string;
}

const LoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [validationErrors, setValidationErrors] = useState<ValidationErrors>({});
  const [touched, setTouched] = useState<{ email: boolean; password: boolean }>({
    email: false,
    password: false,
  });

  const router = useRouter();
  const { signIn } = useAuth();

  // Email validation
  const validateEmail = (email: string): string | undefined => {
    if (!email) {
      return 'Email is required';
    }
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(email)) {
      return 'Please enter a valid email address';
    }
    if (email.length > 254) {
      return 'Email is too long';
    }
    return undefined;
  };

  // Password validation (basic for login - just check if provided)
  const validatePassword = (password: string): string | undefined => {
    if (!password) {
      return 'Password is required';
    }
    if (password.length < 8) {
      return 'Password must be at least 8 characters';
    }
    return undefined;
  };

  // Validate all fields
  const validateForm = (): boolean => {
    const errors: ValidationErrors = {
      email: validateEmail(email),
      password: validatePassword(password),
    };

    setValidationErrors(errors);
    return !errors.email && !errors.password;
  };

  // Handle field blur (mark as touched)
  const handleBlur = (field: 'email' | 'password') => {
    setTouched((prev) => ({ ...prev, [field]: true }));

    // Validate the specific field
    if (field === 'email') {
      const emailError = validateEmail(email);
      setValidationErrors((prev) => ({ ...prev, email: emailError }));
    } else if (field === 'password') {
      const passwordError = validatePassword(password);
      setValidationErrors((prev) => ({ ...prev, password: passwordError }));
    }
  };

  // Handle email change
  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setEmail(value);

    // Clear server error when user starts typing
    if (error) setError('');

    // Validate if field has been touched
    if (touched.email) {
      const emailError = validateEmail(value);
      setValidationErrors((prev) => ({ ...prev, email: emailError }));
    }
  };

  // Handle password change
  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setPassword(value);

    // Clear server error when user starts typing
    if (error) setError('');

    // Validate if field has been touched
    if (touched.password) {
      const passwordError = validatePassword(value);
      setValidationErrors((prev) => ({ ...prev, password: passwordError }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Mark all fields as touched
    setTouched({ email: true, password: true });

    // Validate form
    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      await signIn(email, password);
      router.push('/'); // Redirect to dashboard/home after login
    } catch (err: any) {
      // Parse error message for better user feedback
      let errorMessage = 'Login failed. Please try again.';

      if (err.message) {
        if (err.message.includes('Email not verified')) {
          errorMessage = 'Please verify your email address before logging in.';
        } else if (err.message.includes('Incorrect email or password')) {
          errorMessage = 'Invalid email or password. Please try again.';
        } else if (err.message.includes('Network')) {
          errorMessage = 'Network error. Please check your connection.';
        } else {
          errorMessage = err.message;
        }
      }

      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md p-8 space-y-8 bg-white dark:bg-gray-800 rounded-lg shadow-md">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 dark:text-white">Sign in to your account</h2>
      </div>

      {error && (
        <div className="p-3 text-red-700 bg-red-100 dark:bg-red-900/30 dark:text-red-300 rounded-md border border-red-300 dark:border-red-700">
          <div className="flex items-center">
            <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            {error}
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="mt-8 space-y-6">
        <div className="space-y-4">
          {/* Email Field */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Email address
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              value={email}
              onChange={handleEmailChange}
              onBlur={() => handleBlur('email')}
              disabled={loading}
              className={`block w-full px-3 py-2 mt-1 border rounded-md shadow-sm focus:outline-none focus:ring-2 sm:text-sm transition-colors ${
                touched.email && validationErrors.email
                  ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
                  : 'border-gray-300 dark:border-gray-600 focus:ring-indigo-500 focus:border-indigo-500'
              } ${loading ? 'bg-gray-100 dark:bg-gray-700 cursor-not-allowed' : 'bg-white dark:bg-gray-900'} dark:text-white`}
            />
            {touched.email && validationErrors.email && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">{validationErrors.email}</p>
            )}
          </div>

          {/* Password Field */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              value={password}
              onChange={handlePasswordChange}
              onBlur={() => handleBlur('password')}
              disabled={loading}
              className={`block w-full px-3 py-2 mt-1 border rounded-md shadow-sm focus:outline-none focus:ring-2 sm:text-sm transition-colors ${
                touched.password && validationErrors.password
                  ? 'border-red-500 focus:ring-red-500 focus:border-red-500'
                  : 'border-gray-300 dark:border-gray-600 focus:ring-indigo-500 focus:border-indigo-500'
              } ${loading ? 'bg-gray-100 dark:bg-gray-700 cursor-not-allowed' : 'bg-white dark:bg-gray-900'} dark:text-white`}
            />
            {touched.password && validationErrors.password && (
              <p className="mt-1 text-sm text-red-600 dark:text-red-400">{validationErrors.password}</p>
            )}
          </div>
        </div>

        <div className="flex items-center justify-between">
          <div className="text-sm">
            <a href="/forgot-password" className="font-medium text-indigo-600 dark:text-indigo-400 hover:text-indigo-500 dark:hover:text-indigo-300">
              Forgot your password?
            </a>
          </div>
        </div>

        <div>
          <button
            type="submit"
            disabled={loading || (touched.email && !!validationErrors.email) || (touched.password && !!validationErrors.password)}
            className={`flex justify-center items-center w-full px-4 py-2 text-sm font-medium text-white bg-indigo-600 border border-transparent rounded-md shadow-sm hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all ${
              loading || (touched.email && !!validationErrors.email) || (touched.password && !!validationErrors.password)
                ? 'opacity-50 cursor-not-allowed'
                : ''
            }`}
          >
            {loading && (
              <svg className="w-5 h-5 mr-2 animate-spin" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            )}
            {loading ? 'Signing in...' : 'Sign in'}
          </button>
        </div>

        <div className="text-sm text-center text-gray-500 dark:text-gray-400">
          Don't have an account?{' '}
          <a href="/register" className="font-medium text-indigo-600 dark:text-indigo-400 hover:text-indigo-500 dark:hover:text-indigo-300">
            Sign up
          </a>
        </div>
      </form>
    </div>
  );
};

export default LoginForm;
