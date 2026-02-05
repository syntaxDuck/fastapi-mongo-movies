import Spinner, { SpinnerSize, SpinnerColor, SpinnerType } from "../ui/Spinner";

export { Spinner };
export type { SpinnerSize, SpinnerColor, SpinnerType };

// Pre-configured spinner variants for common use cases
export const LoadingSpinners = {
  // Default loading spinner
  Default: (props?: Partial<Parameters<typeof Spinner>[0]>) => (
    <Spinner size="md" color="primary" type="pulse" {...props} />
  ),

  // Small inline spinner for buttons
  Inline: (props?: Partial<Parameters<typeof Spinner>[0]>) => (
    <Spinner size="sm" color="white" type="dots" inline {...props} />
  ),

  // Large full-page loader
  FullPage: (props?: Partial<Parameters<typeof Spinner>[0]>) => (
    <Spinner size="xl" color="accent" type="ring" {...props} />
  ),

  // Success spinner
  Success: (props?: Partial<Parameters<typeof Spinner>[0]>) => (
    <Spinner size="md" color="success" type="ripple" {...props} />
  ),

  // Error spinner
  Error: (props?: Partial<Parameters<typeof Spinner>[0]>) => (
    <Spinner size="md" color="error" type="bars" {...props} />
  ),

  // Warning spinner
  Warning: (props?: Partial<Parameters<typeof Spinner>[0]>) => (
    <Spinner size="md" color="warning" type="dots" {...props} />
  ),
};

// Loading wrapper component
interface LoadingWrapperProps {
  isLoading: boolean;
  children: React.ReactNode;
  fallback?: React.ReactNode;
  spinnerProps?: Partial<Parameters<typeof Spinner>[0]>;
  className?: string;
}

export const LoadingWrapper: React.FC<LoadingWrapperProps> = ({
  isLoading,
  children,
  fallback,
  spinnerProps = {},
  className = "",
}) => {
  const defaultFallback = <LoadingSpinners.Default {...spinnerProps} />;

  return (
    <div className={className}>
      {isLoading ? (fallback || defaultFallback) : children}
    </div>
  );
};

// Centered loading component
interface CenteredLoadingProps {
  message?: string;
  spinnerProps?: Partial<Parameters<typeof Spinner>[0]>;
  className?: string;
}

export const CenteredLoading: React.FC<CenteredLoadingProps> = ({
  message = "Loading...",
  spinnerProps = {},
  className = "",
}) => {
  return (
    <div 
      className={`flex flex-col items-center justify-center gap-4 ${className}`}
      role="status"
      aria-live="polite"
    >
      <LoadingSpinners.Default {...spinnerProps} />
      {message && (
        <p className="text-secondary text-sm font-medium">{message}</p>
      )}
    </div>
  );
};

// Button loading component
interface ButtonLoadingProps {
  is_loading: boolean;
  children: React.ReactNode;
  spinnerProps?: Partial<Parameters<typeof Spinner>[0]>;
  disabled?: boolean;
  className?: string;
}

export const ButtonLoading: React.FC<ButtonLoadingProps> = ({
  is_loading,
  children,
  spinnerProps = {},
  disabled = false,
  className = "",
}) => {
  return (
    <button 
      disabled={disabled || is_loading}
      className={`${className} ${is_loading ? 'opacity-75 cursor-not-allowed' : ''}`}
      aria-busy={is_loading}
    >
      {is_loading ? (
        <div className="flex items-center gap-2">
          <LoadingSpinners.Inline {...spinnerProps} />
          <span>Loading...</span>
        </div>
      ) : (
        children
      )}
    </button>
  );
};

// Card loading skeleton
interface CardLoadingSkeletonProps {
  count?: number;
  spinnerProps?: Partial<Parameters<typeof Spinner>[0]>;
  className?: string;
}

export const CardLoadingSkeleton: React.FC<CardLoadingSkeletonProps> = ({
  count = 6,
  spinnerProps = {},
  className = "",
}) => {
  return (
    <div className={`${className} grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4`}>
      {Array.from({ length: count }, (_, i) => (
        <div 
          key={i}
          className="aspect-[2/3] bg-surface rounded-lg flex items-center justify-center"
          role="status"
          aria-label={`Loading item ${i + 1}`}
        >
          <LoadingSpinners.Default 
            size="sm" 
            color="gray" 
            type="dots" 
            {...spinnerProps} 
          />
        </div>
      ))}
    </div>
  );
};