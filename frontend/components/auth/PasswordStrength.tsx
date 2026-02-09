/**
 * PasswordStrength component
 *
 * Displays a visual indicator of password strength based on validation criteria.
 */

import { getPasswordStrength, getPasswordStrengthLabel, getPasswordStrengthColor } from '@/lib/validation';

interface PasswordStrengthProps {
  password: string;
}

export function PasswordStrength({ password }: PasswordStrengthProps) {
  const strength = getPasswordStrength(password);
  const label = getPasswordStrengthLabel(password);
  const colorClass = getPasswordStrengthColor(password);

  return (
    <div className="mt-2 space-y-1">
      <div className="flex items-center justify-between">
        <span className="text-xs text-muted-foreground">Password Strength:</span>
        <span className={`text-xs font-medium ${colorClass}`}>{label}</span>
      </div>
      <div className="w-full h-2 bg-secondary rounded-full overflow-hidden">
        <div
          className={`h-full transition-all duration-300 ${
            strength < 40 ? 'bg-red-500' : strength < 70 ? 'bg-yellow-500' : 'bg-green-500'
          }`}
          style={{ width: `${strength}%` }}
        />
      </div>
    </div>
  );
}
