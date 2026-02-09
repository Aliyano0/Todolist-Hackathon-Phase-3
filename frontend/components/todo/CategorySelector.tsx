interface CategorySelectorProps {
  value: string;
  onChange: (value: string) => void;
  predefinedCategories?: string[];
}

export function CategorySelector({
  value,
  onChange,
  predefinedCategories = ['work', 'personal', 'shopping']
}: CategorySelectorProps) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full px-3 py-2 border border-input rounded-md focus:outline-none focus:ring-2 focus:ring-ring"
    >
      {predefinedCategories.map((cat) => (
        <option key={cat} value={cat}>
          {cat.charAt(0).toUpperCase() + cat.slice(1)}
        </option>
      ))}
      <option value="other">Other</option>
    </select>
  );
}