'use client';

import { Button, ButtonProps } from '@/components/ui/button';
import { cn } from '@/lib/utils';

interface AnimatedButtonProps extends ButtonProps {
  glow?: boolean;
  animateOnHover?: boolean;
}

export function AnimatedButton({
  children,
  glow = true,
  animateOnHover = true,
  className,
  ...props
}: AnimatedButtonProps) {
  const buttonClasses = cn(
    className,
    glow && 'glowing-button',
    animateOnHover && 'transition-all duration-200 hover:scale-105 active:scale-95'
  );

  return (
    <Button
      className={buttonClasses}
      {...props}
    >
      {children}
    </Button>
  );
}