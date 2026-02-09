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

// Type exports
export type { ButtonProps } from './Button';
export type { ImageProps } from './Image';
export type { BadgeProps } from './Badge';
export type { 
  SpinnerSize, 
  SpinnerColor, 
  SpinnerType 
} from './Spinner';

// Re-export animation variants for convenience
export { AnimationVariants, getAnimationProps, createStaggeredVariants } from '../../utils/animationVariants';