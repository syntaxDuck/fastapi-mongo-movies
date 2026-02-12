import React, { forwardRef, useId } from "react";
import { motion } from "framer-motion";
import styles from "../../styles/components/ui/Input.module.css";

// Input component interface
export interface InputProps {
  type?: 'text' | 'email' | 'number' | 'search';
  placeholder?: string;
  value?: string | number;
  onChange?: (value: string) => void;
  onClear?: () => void;
  variant?: 'default' | 'search' | 'filter';
  size?: 'sm' | 'md' | 'lg';
  label?: string;
  required?: boolean;
  error?: string;
  disabled?: boolean;
  className?: string;
  id?: string;
  'aria-label'?: string;
  'aria-describedby'?: string;
  onKeyPress?: (e: React.KeyboardEvent<HTMLInputElement>) => void;
  onFocus?: (e: React.FocusEvent<HTMLInputElement>) => void;
  onBlur?: (e: React.FocusEvent<HTMLInputElement>) => void;
}

// Framer Motion variants for input
const inputVariants = {
  idle: { scale: 1 },
  focus: { scale: 1.02 },
  disabled: { opacity: 0.6 }
};

const Input = forwardRef<HTMLInputElement, InputProps>(({
  type = 'text',
  placeholder,
  value = '',
  onChange,
  onClear,
  variant = 'default',
  size = 'md',
  label,
  required = false,
  error,
  disabled = false,
  className,
  id: providedId,
  'aria-label': ariaLabel,
  'aria-describedby': ariaDescribedBy,
  onKeyPress,
  onFocus,
  onBlur
}, ref) => {
  const generatedId = useId();
  const id = providedId || generatedId;

  // Build CSS classes
  const inputClasses = [
    styles.input,
    styles[variant],
    styles[size],
    onClear && styles.hasClearButton,
    error && styles.inputError,
    disabled && styles.inputDisabled,
    className
  ].filter(Boolean).join(' ');

  // Handle input change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    onChange?.(e.target.value);
  };

  return (
    <div className={styles.inputContainer}>
      {label && (
        <label htmlFor={id} className={styles.label}>
          {label}
          {required && <span className={styles.required}>*</span>}
        </label>
      )}
      <motion.div
        className={styles.inputWrapper}
        variants={inputVariants}
        animate={disabled ? "disabled" : "idle"}
        whileFocus="focus"
        transition={{ duration: 0.2 }}
      >
        <input
          ref={ref}
          type={type}
          id={id}
          placeholder={placeholder}
          value={value}
          onChange={handleChange}
          onKeyPress={onKeyPress}
          onFocus={onFocus}
          onBlur={onBlur}
          disabled={disabled}
          className={inputClasses}
          aria-label={ariaLabel}
          aria-describedby={ariaDescribedBy}
          aria-invalid={error ? 'true' : 'false'}
          required={required}
        />
        {onClear && value && (
          <motion.button
            type="button"
            className={styles.clearButton}
            onClick={onClear}
            initial={{ opacity: 0, scale: 0.5 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.5 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            aria-label="Clear input"
          >
            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </motion.button>
        )}
        {error && (
          <motion.div
            className={styles.errorMessage}
            initial={{ opacity: 0, y: -5 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -5 }}
            transition={{ duration: 0.2 }}
          >
            {error}
          </motion.div>
        )}
      </motion.div>
    </div>
  );
});

Input.displayName = 'Input';

export default Input;