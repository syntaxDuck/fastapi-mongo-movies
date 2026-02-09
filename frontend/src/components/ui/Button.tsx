import React from "react";
import { motion } from "framer-motion";
import styles from "../../styles/components/ui/Button.module.css";
import Spinner from "./Spinner";

export interface ButtonProps {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
  disabled?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
  className?: string;
  animation?: "scale" | "slide" | "glow" | "none";
  type?: "button" | "submit" | "reset";
  fullWidth?: boolean;
  id?: string;
  ariaLabel?: string;
}

const Button: React.FC<ButtonProps> = ({
  variant = "primary",
  size = "md",
  loading = false,
  disabled = false,
  children,
  onClick,
  className = "",
  animation = "scale",
  type = "button",
  fullWidth = false,
  id,
  ariaLabel
}) => {
  const buttonClasses = [
    styles.button,
    styles[variant],
    styles[size],
    fullWidth && styles.buttonFullWidth,
    className
  ].filter(Boolean).join(" ");

  const getAnimationProps = () => {
    switch (animation) {
      case "scale":
        return {
          whileHover: { scale: 1.05 },
          whileTap: { scale: 0.95 },
          transition: { duration: 0.2, ease: [0.4, 0, 0.2, 1] } as any
        };
      case "slide":
        return {
          whileHover: { y: -2 },
          whileTap: { y: 0 },
          transition: { duration: 0.2, ease: [0.4, 0, 0.2, 1] } as any
        };
      case "glow":
        return {
          whileHover: { boxShadow: "0 0 20px rgba(59, 130, 246, 0.5)" },
          whileTap: { boxShadow: "0 0 10px rgba(59, 130, 246, 0.3)" },
          transition: { duration: 0.2 } as any
        };
      default:
        return {};
    }
  };

  const getSpinnerColor = (): "primary" | "accent" | "success" | "warning" | "error" | "white" | "gray" => {
    switch (variant) {
      case "primary":
      case "danger":
        return "white";
      case "secondary":
      case "ghost":
        return "primary";
      default:
        return "white";
    }
  };

  return (
    <motion.button
      id={id}
      className={buttonClasses}
      disabled={disabled || loading}
      onClick={onClick}
      type={type}
      aria-label={ariaLabel}
      aria-busy={loading}
      {...getAnimationProps()}
    >
      {loading ? (
        <div className={styles.buttonLoading}>
          <Spinner
            size="sm"
            color={getSpinnerColor()}
            type="dots"
            inline
          />
          <span>Loading...</span>
        </div>
      ) : (
        children
      )}
    </motion.button>
  );
};

export default Button;
