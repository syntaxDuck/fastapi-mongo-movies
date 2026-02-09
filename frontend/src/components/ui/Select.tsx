import React, { useId } from "react";
import styles from "../../styles/components/ui/Select.module.css";

export interface SelectOption {
  value: string | number;
  label: string;
}

export interface SelectProps {
  options: SelectOption[];
  value: string | number | string[];
  onChange: (value: string | number | string[]) => void;
  label?: string;
  placeholder?: string;
  multi?: boolean;
  disabled?: boolean;
  error?: string;
  required?: boolean;
  className?: string;
  id?: string;
  variant?: "default" | "filter" | "outline";
  size?: "sm" | "md" | "lg";
}

const Select: React.FC<SelectProps> = ({
  options,
  value,
  onChange,
  label,
  placeholder = "Select an option",
  multi = false,
  disabled = false,
  error,
  required = false,
  className = "",
  id: providedId,
  variant = "default",
  size = "md",
}) => {
  const generatedId = useId();
  const id = providedId || generatedId;

  const selectClasses = [
    styles.select,
    styles[variant],
    styles[size],
    error && styles.selectError,
    disabled && styles.selectDisabled,
    className,
  ]
    .filter(Boolean)
    .join(" ");

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    if (multi) {
      const values = Array.from(
        e.target.selectedOptions,
        (option) => option.value
      );
      onChange(values);
    } else {
      onChange(e.target.value);
    }
  };

  return (
    <div className={styles.selectContainer}>
      {label && (
        <label htmlFor={id} className={styles.label}>
          {label}
          {required && <span className={styles.required}>*</span>}
        </label>
      )}
      <div className={styles.selectWrapper}>
        <select
          id={id}
          value={value}
          onChange={handleChange}
          multiple={multi}
          disabled={disabled}
          required={required}
          className={selectClasses}
        >
          {!multi && placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        <div className={styles.selectIcon}>▼</div>
      </div>
      {error && <span className={styles.errorText}>{error}</span>}
    </div>
  );
};

export default Select;
