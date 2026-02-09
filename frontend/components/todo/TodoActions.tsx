import { Button } from '@/components/ui/button';
import { Trash2, CheckCircle, Circle } from 'lucide-react';

interface TodoActionsProps {
  completed: boolean;
  onToggleComplete: () => void;
  onDelete: () => void;
}

export function TodoActions({ completed, onToggleComplete, onDelete }: TodoActionsProps) {
  return (
    <div className="flex space-x-2">
      <Button
        variant="ghost"
        size="sm"
        onClick={onToggleComplete}
        className="p-2 hover:bg-transparent"
        aria-label={completed ? 'Mark as incomplete' : 'Mark as complete'}
      >
        {completed ? (
          <CheckCircle className="h-4 w-4 text-green-500" />
        ) : (
          <Circle className="h-4 w-4 text-muted-foreground" />
        )}
      </Button>
      <Button
        variant="ghost"
        size="sm"
        onClick={onDelete}
        className="p-2 hover:bg-transparent text-destructive"
        aria-label="Delete todo"
      >
        <Trash2 className="h-4 w-4" />
      </Button>
    </div>
  );
}