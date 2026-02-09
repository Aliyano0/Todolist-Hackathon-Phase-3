import { cn } from '@/lib/utils';

interface HoverEffectProps {
  children: React.ReactNode;
  className?: string;
}

export function HoverEffect({ children, className }: HoverEffectProps) {
  return (
    <div
      className={cn(
        'transition-all duration-200 ease-in-out hover:shadow-md cursor-pointer',
        className
      )}
    >
      {children}
    </div>
  );
}