// UI Components Barrel Export
// Provides clean import paths for all UI components

// Component exports
export { default as Button } from './Button';
export { default as Image } from './Image';
export { default as Badge } from './Badge';
export { default as Spinner } from './Spinner';
export { 
  LoadingSpinners,
  LoadingWrapper,
  CenteredLoading,
  ButtonLoading,
  CardLoadingSkeleton
} from './LoadingComponents';

// Form and input components
export { default as Input } from './Input';
export { default as Select } from './Select';
export { default as RangeInput } from './RangeInput';
export { default as SearchMenu } from './SearchMenu';

// Type exports
export type { ButtonProps } from './Button';
export type { ImageProps } from './Image';
export type { BadgeProps } from './Badge';
export type { 
  SpinnerSize, 
  SpinnerColor, 
  SpinnerType 
} from './Spinner';

// Form and input component types
export type { InputProps } from './Input';
export type { SelectProps } from './Select';
export type { RangeInputProps } from './RangeInput';
export type { SearchMenuProps } from './SearchMenu';

// Re-export animation variants for convenience
export { AnimationVariants, getAnimationProps, createStaggeredVariants } from '../../utils/animationVariants';