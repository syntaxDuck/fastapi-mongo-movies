import React, { forwardRef } from "react";
import { motion } from "framer-motion";
import styles from "../../styles/components/ui/RangeInput.module.css";

// RangeInput component interface
export interface RangeInputProps {
  min?: number;
  max?: number;
  value?: { min: number; max: number };
  onChange?: (range: { min: number; max: number }) => void;
  placeholder?: { min: string; max: string };
  error?: string;
  className?: string;
  label?: string;
  disabled?: boolean;
  id?: string;
  'aria-label'?: string;
  'aria-describedby'?: string;
}

// Framer Motion variants for range input
const rangeVariants = {
  idle: { scale: 1 },
  focus: { scale: 1.02 },
  disabled: { opacity: 0.6 }
};

const RangeInput = forwardRef<HTMLDivElement, RangeInputProps>(({
  min = 0,
  max = 100,
  value = { min: min, max: max },
  onChange,
  placeholder = { min: "Min", max: "Max" },
  error,
  className,
  label,
  disabled = false,
  id,
  'aria-label': ariaLabel,
  'aria-describedby': ariaDescribedBy
}, ref) => {
  // Handle min value change
  const handleMinChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newMin = parseInt(e.target.value) || min;
    const newMax = Math.max(newMin, value?.max || max);
    onChange?.({ min: newMin, max: newMax });
  };

  // Handle max value change
  const handleMaxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newMax = parseInt(e.target.value) || max;
    const newMin = Math.min(newMax, value?.min || min);
    onChange?.({ min: newMin, max: newMax });
  };

  // Validate range
  const validateRange = (val: number, type: 'min' | 'max') => {
    if (type === 'min') {
      return val >= min && val <= (value?.max || max);
    } else {
      return val <= max && val >= (value?.min || min);
    }
  };

  // Check if values are valid
  const isMinValid = value?.min !== undefined ? validateRange(value.min, 'min') : true;
  const isMaxValid = value?.max !== undefined ? validateRange(value.max, 'max') : true;

  // Build CSS classes
  const rangeClasses = [
    styles.rangeInput,
    error && styles.rangeError,
    disabled && styles.rangeDisabled,
    className
  ].filter(Boolean).join(' ');

  const inputClasses = [
    styles.rangeField,
    !isMinValid && styles.fieldError,
    !isMaxValid && styles.fieldError
  ].filter(Boolean).join(' ');

  return (
    <motion.div
      ref={ref}
      id={id}
      className={rangeClasses}
      variants={rangeVariants}
      animate={disabled ? "disabled" : "idle"}
      whileFocus="focus"
      transition={{ duration: 0.2 }}
      aria-label={ariaLabel}
      aria-describedby={ariaDescribedBy}
    >
      {label && (
        <label className={styles.rangeLabel}>
          {label}
        </label>
      )}
      
      <div className={styles.rangeFields}>
        <div className={styles.rangeFieldGroup}>
          <motion.input
            type="number"
            min={min}
            max={value?.max || max}
            value={value?.min ?? ''}
            onChange={handleMinChange}
            placeholder={placeholder.min}
            disabled={disabled}
            className={`${inputClasses} ${styles.minField}`}
            aria-label={`Minimum ${label || 'value'}`}
            aria-invalid={!isMinValid ? 'true' : 'false'}
            whileFocus={{ scale: 1.02 }}
            transition={{ duration: 0.2 }}
          />
          <span className={styles.rangeSeparator}>—</span>
          <motion.input
            type="number"
            min={value?.min || min}
            max={max}
            value={value?.max ?? ''}
            onChange={handleMaxChange}
            placeholder={placeholder.max}
            disabled={disabled}
            className={`${inputClasses} ${styles.maxField}`}
            aria-label={`Maximum ${label || 'value'}`}
            aria-invalid={!isMaxValid ? 'true' : 'false'}
            whileFocus={{ scale: 1.02 }}
            transition={{ duration: 0.2 }}
          />
        </div>
      </div>

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

      {/* Range validation errors */}
      {!isMinValid && (
        <motion.div
          className={styles.errorMessage}
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
        >
          Minimum value must be between {min} and {value?.max || max}
        </motion.div>
      )}

      {!isMaxValid && (
        <motion.div
          className={styles.errorMessage}
          initial={{ opacity: 0, y: -5 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
        >
          Maximum value must be between {value?.min || min} and {max}
        </motion.div>
      )}
    </motion.div>
  );
});

RangeInput.displayName = 'RangeInput';

export default RangeInput;