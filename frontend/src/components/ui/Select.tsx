import React, { useState, useRef, useEffect, useCallback, forwardRef, useId } from "react";
import { motion, AnimatePresence } from "framer-motion";
import styles from "../../styles/components/ui/Select.module.css";

// Select component interface
export interface SelectProps {
  options: { value: string | number; label: string }[];
  value?: string | number | (string | number)[];
  onChange?: (value: string | number | (string | number)[]) => void;
  placeholder?: string;
  multi?: boolean;
  variant?: 'default' | 'filter';
  size?: 'sm' | 'md' | 'lg';
  label?: string;
  required?: boolean;
  error?: string;
  disabled?: boolean;
  className?: string;
  id?: string;
  'aria-label'?: string;
  'aria-describedby'?: string;
}

// Framer Motion variants for select
const selectVariants = {
  idle: { scale: 1 },
  focus: { scale: 1.02 },
  disabled: { opacity: 0.6 }
};

const dropdownVariants = {
  hidden: {
    opacity: 0,
    y: -10,
    transition: { duration: 0.2 }
  },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.2 }
  },
  exit: {
    opacity: 0,
    y: -10,
    transition: { duration: 0.2 }
  }
};

const optionVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: { opacity: 1, x: 0 },
  hover: {
    scale: 1.02,
    backgroundColor: "var(--bg-hover)",
    transition: { duration: 0.1 }
  }
};

const Select = forwardRef<HTMLDivElement, SelectProps>(({
  options,
  value,
  onChange,
  placeholder = "Select an option...",
  multi = false,
  variant = 'default',
  size = 'md',
  label,
  required = false,
  error,
  disabled = false,
  className,
  id: providedId,
  'aria-label': ariaLabel,
  'aria-describedby': ariaDescribedBy
}, ref) => {
  const generatedId = useId();
  const id = providedId || generatedId;
  const [isOpen, setIsOpen] = useState(false);
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Handle click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  // Handle option selection
  const handleOptionSelect = useCallback((optionValue: string | number) => {
    if (multi) {
      const currentValues = Array.isArray(value) ? value : [];
      const newValues = currentValues.includes(optionValue)
        ? currentValues.filter(v => v !== optionValue)
        : [...currentValues, optionValue];
      onChange?.(newValues);
    } else {
      onChange?.(optionValue);
      setIsOpen(false);
    }
  }, [multi, value, onChange]);

  // Handle keyboard navigation
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (!isOpen) return;

      switch (event.key) {
        case 'ArrowDown':
          event.preventDefault();
          setHighlightedIndex(prev =>
            prev < options.length - 1 ? prev + 1 : 0
          );
          break;
        case 'ArrowUp':
          event.preventDefault();
          setHighlightedIndex(prev =>
            prev > 0 ? prev - 1 : options.length - 1
          );
          break;
        case 'Enter':
          event.preventDefault();
          if (highlightedIndex >= 0) {
            handleOptionSelect(options[highlightedIndex].value);
          }
          break;
        case 'Escape':
          setIsOpen(false);
          break;
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
    }

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, highlightedIndex, options, handleOptionSelect]);

  // Handle toggle dropdown
  const toggleDropdown = () => {
    if (!disabled) {
      setIsOpen(!isOpen);
      setHighlightedIndex(-1);
    }
  };

  // Get display text
  const getDisplayText = () => {
    if (multi) {
      const selectedValues = Array.isArray(value) ? value : [];
      if (selectedValues.length === 0) return placeholder;
      if (selectedValues.length === 1) {
        const option = options.find(o => o.value === selectedValues[0]);
        return option?.label || placeholder;
      }
      return `${selectedValues.length} items selected`;
    } else {
      if (value === undefined || value === null || value === '') return placeholder;
      const option = options.find(o => o.value === value);
      return option?.label || placeholder;
    }
  };

  // Check if option is selected
  const isOptionSelected = (optionValue: string | number) => {
    if (multi) {
      const selectedValues = Array.isArray(value) ? value : [];
      return selectedValues.includes(optionValue);
    }
    return value === optionValue;
  };

  // Build CSS classes
  const selectClasses = [
    styles.select,
    styles[variant],
    styles[size],
    isOpen && styles.selectOpen,
    error && styles.selectError,
    disabled && styles.selectDisabled,
    className
  ].filter(Boolean).join(' ');

  return (
    <div className={styles.selectContainer}>
      {label && (
        <label htmlFor={id} className={styles.label}>
          {label}
          {required && <span className={styles.required}>*</span>}
        </label>
      )}
      <motion.div
        ref={containerRef}
        className={styles.selectWrapper}
        variants={selectVariants}
        animate={disabled ? "disabled" : "idle"}
        whileFocus="focus"
        transition={{ duration: 0.2 }}
      >
        <div
          ref={ref}
          id={id}
          className={selectClasses}
          onClick={toggleDropdown}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              toggleDropdown();
            }
          }}
          role="combobox"
          aria-label={ariaLabel}
          aria-describedby={ariaDescribedBy}
          aria-expanded={isOpen}
          aria-haspopup="listbox"
          aria-controls={isOpen ? `${id}-dropdown` : undefined}
          tabIndex={disabled ? -1 : 0}
        >
          <span className={styles.selectValue}>
            {getDisplayText()}
          </span>
          <motion.span
            className={styles.selectArrow}
            animate={{ rotate: isOpen ? 180 : 0 }}
            transition={{ duration: 0.2 }}
          >
            ▼
          </motion.span>
        </div>

        <AnimatePresence>
          {isOpen && (
            <motion.div
              ref={dropdownRef}
              id={`${id}-dropdown`}
              className={styles.dropdown}
              variants={dropdownVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              role="listbox"
            >
              {options.map((option, index) => (
                <motion.div
                  key={option.value}
                  className={`${styles.option} ${isOptionSelected(option.value) ? styles.optionSelected : ''}`}
                  onClick={() => handleOptionSelect(option.value)}
                  variants={optionVariants}
                  initial="hidden"
                  animate="visible"
                  whileHover="hover"
                  custom={index}
                  role="option"
                  aria-selected={isOptionSelected(option.value)}
                >
                  {multi && (
                    <span className={styles.checkbox}>
                      {isOptionSelected(option.value) ? '✓' : ''}
                    </span>
                  )}
                  <span className={styles.optionLabel}>{option.label}</span>
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

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

Select.displayName = 'Select';

export default Select;