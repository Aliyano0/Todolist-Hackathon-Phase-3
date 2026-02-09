import { PriorityLevel } from '@/lib/api';

interface PrioritySelectorProps {
  value: PriorityLevel;
  onChange: (value: PriorityLevel) => void;
}

export function PrioritySelector({ value, onChange }: PrioritySelectorProps) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value as PriorityLevel)}
      className="w-full px-3 py-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring"
    >
      <option value="low">Low</option>
      <option value="medium">Medium</option>
      <option value="high">High</option>
    </select>
  );
}