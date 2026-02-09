/**
 * Tests for RegisterForm component
 *
 * Tests user registration form functionality including:
 * - Form rendering
 * - Input validation
 * - Password strength indicator
 * - Form submission
 * - Error handling
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import { RegisterForm } from '@/components/auth/RegisterForm';

// Mock Next.js router
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
    replace: jest.fn(),
  }),
}));

// Mock fetch
global.fetch = jest.fn();

describe('RegisterForm', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders registration form with all fields', () => {
    render(<RegisterForm />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /register/i })).toBeInTheDocument();
  });

  it('shows validation error for invalid email', async () => {
    render(<RegisterForm />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    fireEvent.change(emailInput, { target: { value: 'invalid-email' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/valid email/i)).toBeInTheDocument();
    });
  });

  it('shows validation error for weak password', async () => {
    render(<RegisterForm />);

    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    fireEvent.change(passwordInput, { target: { value: 'weak' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/at least 8 characters/i)).toBeInTheDocument();
    });
  });

  it('shows password strength indicator', () => {
    render(<RegisterForm />);

    const passwordInput = screen.getByLabelText(/password/i);

    fireEvent.change(passwordInput, { target: { value: 'TestPass123!' } });

    expect(screen.getByText(/password strength/i)).toBeInTheDocument();
  });

  it('submits form with valid data', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        id: '123',
        email: 'test@example.com',
        email_verified: false,
      }),
    });

    render(<RegisterForm />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'TestPass123!' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/auth/register'),
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({
            email: 'test@example.com',
            password: 'TestPass123!',
          }),
        })
      );
    });
  });

  it('displays error message on registration failure', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      json: async () => ({
        detail: 'Email already registered',
      }),
    });

    render(<RegisterForm />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'TestPass123!' } });
    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/email already registered/i)).toBeInTheDocument();
    });
  });

  it('disables submit button while submitting', async () => {
    (global.fetch as jest.Mock).mockImplementation(
      () => new Promise((resolve) => setTimeout(resolve, 100))
    );

    render(<RegisterForm />);

    const emailInput = screen.getByLabelText(/email/i);
    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    fireEvent.change(emailInput, { target: { value: 'test@example.com' } });
    fireEvent.change(passwordInput, { target: { value: 'TestPass123!' } });
    fireEvent.click(submitButton);

    expect(submitButton).toBeDisabled();
  });

  it('validates all password requirements', async () => {
    render(<RegisterForm />);

    const passwordInput = screen.getByLabelText(/password/i);
    const submitButton = screen.getByRole('button', { name: /register/i });

    // Test missing uppercase
    fireEvent.change(passwordInput, { target: { value: 'lowercase123!' } });
    fireEvent.click(submitButton);
    await waitFor(() => {
      expect(screen.getByText(/uppercase/i)).toBeInTheDocument();
    });

    // Test missing lowercase
    fireEvent.change(passwordInput, { target: { value: 'UPPERCASE123!' } });
    fireEvent.click(submitButton);
    await waitFor(() => {
      expect(screen.getByText(/lowercase/i)).toBeInTheDocument();
    });

    // Test missing number
    fireEvent.change(passwordInput, { target: { value: 'NoNumbers!' } });
    fireEvent.click(submitButton);
    await waitFor(() => {
      expect(screen.getByText(/number/i)).toBeInTheDocument();
    });

    // Test missing special character
    fireEvent.change(passwordInput, { target: { value: 'NoSpecial123' } });
    fireEvent.click(submitButton);
    await waitFor(() => {
      expect(screen.getByText(/special/i)).toBeInTheDocument();
    });
  });
});
