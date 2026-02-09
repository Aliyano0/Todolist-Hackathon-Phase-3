// Design System Tokens for Professional Frontend UI Upgrade
// Feature: 020-frontend-ui-upgrade

export const colors = {
  priority: {
    high: '#EF4444',
    medium: '#F59E0B',
    low: '#10B981',
    none: '#6B7280'
  },
  category: {
    work: '#3B82F6',
    personal: '#8B5CF6',
    shopping: '#EC4899',
    health: '#10B981',
    other: '#6B7280'
  }
} as const

export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px',
  '2xl': '48px',
  '3xl': '64px'
} as const

export const typography = {
  fontSize: {
    xs: '12px',
    sm: '14px',
    base: '16px',
    lg: '18px',
    xl: '20px',
    '2xl': '24px',
    '3xl': '32px',
    '4xl': '36px',
    '5xl': '48px'
  },
  lineHeight: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.75
  },
  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700
  }
} as const

export const animations = {
  duration: {
    fast: 150,
    normal: 200,
    medium: 250,
    slow: 300
  },
  easing: {
    easeInOut: [0.4, 0, 0.2, 1] as const,
    easeOut: [0, 0, 0.2, 1] as const,
    easeIn: [0.4, 0, 1, 1] as const
  },
  spring: {
    default: { stiffness: 300, damping: 30 },
    gentle: { stiffness: 200, damping: 25 },
    stiff: { stiffness: 400, damping: 35 }
  }
} as const

// Type exports for TypeScript
export type PriorityColor = keyof typeof colors.priority
export type CategoryColor = keyof typeof colors.category
export type SpacingToken = keyof typeof spacing
export type FontSize = keyof typeof typography.fontSize
export type FontWeight = keyof typeof typography.fontWeight
export type AnimationDuration = keyof typeof animations.duration
