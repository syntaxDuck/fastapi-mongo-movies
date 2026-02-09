import React, { useId } from "react";
import styles from "../../styles/components/ui/RangeInput.module.css";
import Input from "./Input";

export interface RangeValue {
  min: number;
  max: number;
}

export interface RangeInputProps {
  label?: string;
  min: number;
  max: number;
  value: RangeValue;
  onChange: (value: RangeValue) => void;
  step?: number;
  placeholder?: {
    min: string;
    max: string;
  };
  disabled?: boolean;
  className?: string;
}

const RangeInput: React.FC<RangeInputProps> = ({
  label,
  min,
  max,
  value,
  onChange,
  placeholder,
  disabled = false,
  className = "",
}) => {
  const minId = useId();
  const maxId = useId();

  const handleMinChange = (newMin: string) => {
    const val = parseInt(newMin) || min;
    onChange({ ...value, min: Math.min(val, value.max) });
  };

  const handleMaxChange = (newMax: string) => {
    const val = parseInt(newMax) || max;
    onChange({ ...value, max: Math.max(val, value.min) });
  };

  const containerClasses = [styles.rangeContainer, className]
    .filter(Boolean)
    .join(" ");

  return (
    <fieldset className={containerClasses} disabled={disabled}>
      {label && <legend className={styles.label}>{label}</legend>}
      <div className={styles.rangeInputs}>
        <Input
          id={minId}
          type="number"
          value={value.min}
          onChange={handleMinChange}
          placeholder={placeholder?.min}
          variant="outline"
          className={styles.rangeField}
          label="Min"
        />
        <span className={styles.rangeSeparator}>—</span>
        <Input
          id={maxId}
          type="number"
          value={value.max}
          onChange={handleMaxChange}
          placeholder={placeholder?.max}
          variant="outline"
          className={styles.rangeField}
          label="Max"
        />
      </div>
    </fieldset>
  );
};

export default RangeInput;
