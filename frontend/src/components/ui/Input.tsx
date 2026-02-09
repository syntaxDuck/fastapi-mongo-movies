import React, { useId } from "react";
import styles from "../../styles/components/ui/Input.module.css";

export interface InputProps {
  type?: "text" | "password" | "email" | "number" | "search" | "tel" | "url";
  placeholder?: string;
  value: string | number;
  onChange: (value: string) => void;
  label?: string;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
  id?: string;
  name?: string;
  autoComplete?: string;
  onKeyPress?: (e: React.KeyboardEvent<HTMLInputElement>) => void;
  variant?: "default" | "search" | "outline";
}

const Input: React.FC<InputProps> = ({
  type = "text",
  placeholder,
  value,
  onChange,
  label,
  error,
  required = false,
  disabled = false,
  className = "",
  id: providedId,
  name,
  autoComplete,
  onKeyPress,
  variant = "default",
}) => {
  const generatedId = useId();
  const id = providedId || generatedId;

  const inputClasses = [
    styles.input,
    styles[variant],
    error && styles.inputError,
    disabled && styles.inputDisabled,
    className,
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <div className={styles.inputContainer}>
      {label && (
        <label htmlFor={id} className={styles.label}>
          {label}
          {required && <span className={styles.required}>*</span>}
        </label>
      )}
      <input
        id={id}
        name={name}
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyPress={onKeyPress}
        placeholder={placeholder}
        disabled={disabled}
        required={required}
        autoComplete={autoComplete}
        className={inputClasses}
      />
      {error && <span className={styles.errorText}>{error}</span>}
    </div>
  );
};

export default Input;
