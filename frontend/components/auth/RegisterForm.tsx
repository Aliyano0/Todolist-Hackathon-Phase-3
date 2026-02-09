'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/providers/AuthProvider';

interface ValidationErrors {
  email?: string;
  password?: string;
  confirmPassword?: string;
}

interface PasswordStrength {
  score: number; // 0-4
  label: string;
  color: string;
}

const RegisterForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [validationErrors, setValidationErrors] = useState<ValidationErrors>({});
  const [touched, setTouched] = useState<{ email: boolean; password: boolean; confirmPassword: boolean }>({
    email: false,
    password: false,
    confirmPassword: false,
  });
  const [showPassword, setShowPassword] = useState(false);

  const router = useRouter();
  const { signUp } = useAuth();

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

  // Password strength calculation
  const calculatePasswordStrength = (password: string): PasswordStrength => {
    let score = 0;

    if (password.length >= 8) score++;
    if (password.length >= 12) score++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score++;

    const labels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
    const colors = ['bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-blue-500', 'bg-green-500'];

    return {
      score: Math.min(score, 4),
      label: labels[Math.min(score, 4)],
      color: colors[Math.min(score, 4)]
    };
  };

  // Password validation
  const validatePassword = (password: string): string | undefined => {
    if (!password) {
      return 'Password is required';
    }
    if (password.length < 8) {
      return 'Password must be at least 8 characters';
    }
    if (password.length > 128) {
      return 'Password must not exceed 128 characters';
    }
    if (!/[A-Z]/.test(password)) {
      return 'Password must contain at least one uppercase letter';
    }
    if (!/[a-z]/.test(password)) {
      return 'Password must contain at least one lowercase letter';
    }
    if (!/[0-9]/.test(password)) {
      return 'Password must contain at least one number';
    }
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      return 'Password must contain at least one special character';
    }
    return undefined;
  };

  // Confirm password validation
  const validateConfirmPassword = (confirmPassword: string): string | undefined => {
    if (!confirmPassword) {
      return 'Please confirm your password';
    }
    if (confirmPassword !== password) {
      return 'Passwords do not match';
    }
    return undefined;
  };

  // Validate all fields
  const validateForm = (): boolean => {
    const errors: ValidationErrors = {
      email: validateEmail(email),
      password: validatePassword(password),
      confirmPassword: validateConfirmPassword(confirmPassword),
    };

    setValidationErrors(errors);
    return !errors.email && !errors.password && !errors.confirmPassword;
  };

  // Handle field blur
  const handleBlur = (field: 'email' | 'password' | 'confirmPassword') => {
    setTouched((prev) => ({ ...prev, [field]: true }));

    if (field === 'email') {
      const emailError = validateEmail(email);
      setValidationErrors((prev) => ({ ...prev, email: emailError }));
    } else if (field === 'password') {
      const passwordError = validatePassword(password);
      setValidationErrors((prev) => ({ ...prev, password: passwordError }));
    } else if (field === 'confirmPassword') {
      const confirmError = validateConfirmPassword(confirmPassword);
      setValidationErrors((prev) => ({ ...prev, confirmPassword: confirmError }));
    }
  };

  // Handle email change
  const handleEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setEmail(value);
    if (error) setError('');
    if (touched.email) {
      const emailError = validateEmail(value);
      setValidationErrors((prev) => ({ ...prev, email: emailError }));
    }
  };

  // Handle password change
  const handlePasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setPassword(value);
    if (error) setError('');
    if (touched.password) {
      const passwordError = validatePassword(value);
      setValidationErrors((prev) => ({ ...prev, password: passwordError }));
    }
    // Re-validate confirm password if it's been touched
    if (touched.confirmPassword && confirmPassword) {
      const confirmError = value !== confirmPassword ? 'Passwords do not match' : undefined;
      setValidationErrors((prev) => ({ ...prev, confirmPassword: confirmError }));
    }
  };

  // Handle confirm password change
  const handleConfirmPasswordChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setConfirmPassword(value);
    if (error) setError('');
    if (touched.confirmPassword) {
      const confirmError = validateConfirmPassword(value);
      setValidationErrors((prev) => ({ ...prev, confirmPassword: confirmError }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    // Mark all fields as touched
    setTouched({ email: true, password: true, confirmPassword: true });

    // Validate form
    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      await signUp(email, password);
      router.push('/'); // Redirect after registration
    } catch (err: any) {
      let errorMessage = 'Registration failed. Please try again.';

      if (err.message) {
        if (err.message.includes('already exists')) {
          errorMessage = 'An account with this email already exists.';
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

  const passwordStrength = password ? calculatePasswordStrength(password) : null;

  return (
    <div className="w-full max-w-md p-8 space-y-8 bg-card rounded-lg shadow-lg border border-border">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-foreground">Create an account</h2>
      </div>

      {error && (
        <div className="p-3 text-destructive bg-destructive/10 rounded-lg border border-destructive/30">
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
            <label htmlFor="email" className="block text-sm font-medium text-foreground">
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
              className={`block w-full px-3 py-2 mt-1 border rounded-lg shadow-sm focus:outline-none focus:ring-2 sm:text-sm transition-colors bg-background text-foreground ${
                touched.email && validationErrors.email
                  ? 'border-destructive focus:ring-destructive focus:border-destructive'
                  : 'border-input focus:ring-ring focus:border-ring'
              } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
            />
            {touched.email && validationErrors.email && (
              <p className="mt-1 text-sm text-destructive">{validationErrors.email}</p>
            )}
          </div>

          {/* Password Field */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-foreground">
              Password
            </label>
            <div className="relative">
              <input
                id="password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                autoComplete="new-password"
                value={password}
                onChange={handlePasswordChange}
                onBlur={() => handleBlur('password')}
                disabled={loading}
                className={`block w-full px-3 py-2 mt-1 border rounded-lg shadow-sm focus:outline-none focus:ring-2 sm:text-sm transition-colors bg-background text-foreground pr-10 ${
                  touched.password && validationErrors.password
                    ? 'border-destructive focus:ring-destructive focus:border-destructive'
                    : 'border-input focus:ring-ring focus:border-ring'
                } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-0 flex items-center pr-3 mt-1"
              >
                {showPassword ? (
                  <svg className="w-5 h-5 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                  </svg>
                ) : (
                  <svg className="w-5 h-5 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                  </svg>
                )}
              </button>
            </div>

            {/* Password Strength Indicator */}
            {password && passwordStrength && (
              <div className="mt-2">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-muted-foreground">Password strength:</span>
                  <span className="text-xs font-medium text-foreground">{passwordStrength.label}</span>
                </div>
                <div className="w-full h-2 bg-muted rounded-full overflow-hidden">
                  <div
                    className={`h-full ${passwordStrength.color} transition-all duration-300`}
                    style={{ width: `${(passwordStrength.score + 1) * 20}%` }}
                  />
                </div>
              </div>
            )}

            {touched.password && validationErrors.password && (
              <p className="mt-1 text-sm text-destructive">{validationErrors.password}</p>
            )}

            {!validationErrors.password && (
              <p className="mt-1 text-xs text-muted-foreground">
                Must be 8+ characters with uppercase, lowercase, number, and special character
              </p>
            )}
          </div>

          {/* Confirm Password Field */}
          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-foreground">
              Confirm Password
            </label>
            <input
              id="confirmPassword"
              name="confirmPassword"
              type={showPassword ? 'text' : 'password'}
              autoComplete="new-password"
              value={confirmPassword}
              onChange={handleConfirmPasswordChange}
              onBlur={() => handleBlur('confirmPassword')}
              disabled={loading}
              className={`block w-full px-3 py-2 mt-1 border rounded-lg shadow-sm focus:outline-none focus:ring-2 sm:text-sm transition-colors bg-background text-foreground ${
                touched.confirmPassword && validationErrors.confirmPassword
                  ? 'border-destructive focus:ring-destructive focus:border-destructive'
                  : 'border-input focus:ring-ring focus:border-ring'
              } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
            />
            {touched.confirmPassword && validationErrors.confirmPassword && (
              <p className="mt-1 text-sm text-destructive">{validationErrors.confirmPassword}</p>
            )}
            {touched.confirmPassword && !validationErrors.confirmPassword && confirmPassword && (
              <p className="mt-1 text-sm text-green-600 dark:text-green-400 flex items-center">
                <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Passwords match
              </p>
            )}
          </div>
        </div>

        <div>
          <button
            type="submit"
            disabled={loading || Object.values(validationErrors).some(error => error !== undefined)}
            className={`flex justify-center items-center w-full px-4 py-2 text-sm font-medium text-primary-foreground bg-primary border border-transparent rounded-lg shadow-sm hover:bg-primary/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-ring transition-all ${
              loading || Object.values(validationErrors).some(error => error !== undefined)
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
            {loading ? 'Creating account...' : 'Sign up'}
          </button>
        </div>

        <div className="text-sm text-center text-muted-foreground">
          Already have an account?{' '}
          <a href="/login" className="font-medium text-primary hover:text-primary/80 transition-colors">
            Sign in
          </a>
        </div>
      </form>
    </div>
  );
};

export default RegisterForm;
