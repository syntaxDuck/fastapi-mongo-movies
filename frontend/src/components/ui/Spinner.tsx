import React from "react";
import { motion } from "framer-motion";
import styles from "../../styles/components/ui/Spinner.module.css";

// Spinner size variants
export type SpinnerSize = "xs" | "sm" | "md" | "lg" | "xl";

// Spinner color variants
export type SpinnerColor = "primary" | "accent" | "success" | "warning" | "error" | "white" | "gray";

// Spinner type variants
export type SpinnerType = "pulse" | "dots" | "bars" | "ring" | "ripple";

interface SpinnerProps {
  /** Size of the spinner */
  size?: SpinnerSize;
  /** Color theme of the spinner */
  color?: SpinnerColor;
  /** Type of animation */
  type?: SpinnerType;
  /** Optional custom className */
  className?: string;
  /** Optional label for accessibility */
  label?: string;
  /** Whether to show the spinner inline */
  inline?: boolean;
}

const Spinner: React.FC<SpinnerProps> = ({
  size = "md",
  color = "primary",
  type = "pulse",
  className = "",
  label,
  inline = false,
}) => {
  const getAriaLabel = () => {
    if (label) return label;
    return `Loading...`;
  };

  const spinnerClasses = [
    styles.spinner,
    styles[size],
    styles[color],
    inline && styles.inline,
    className,
  ].filter(Boolean).join(" ");

  const renderSpinner = () => {
    switch (type) {
      case "dots":
        return (
          <div className={styles.dotsContainer}>
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className={styles.dot}
                animate={{
                  scale: [1, 1.3, 1],
                  opacity: [0.5, 1, 0.5],
                }}
                transition={{
                  duration: 1.4,
                  repeat: Infinity,
                  delay: i * 0.16,
                  ease: "easeInOut",
                }}
              />
            ))}
          </div>
        );
      
      case "bars":
        return (
          <div className={styles.barsContainer}>
            {[0, 1, 2, 3].map((i) => (
              <motion.div
                key={i}
                className={styles.bar}
                animate={{
                  scaleY: [0.4, 1, 0.4],
                  opacity: [0.6, 1, 0.6],
                }}
                transition={{
                  duration: 1.2,
                  repeat: Infinity,
                  delay: i * 0.1,
                  ease: "easeInOut",
                }}
              />
            ))}
          </div>
        );
      
      case "ring":
        return (
          <div className={styles.ringContainer}>
            <motion.div
              className={styles.ringOuter}
              animate={{
                rotate: 360,
              }}
              transition={{
                duration: 1.5,
                repeat: Infinity,
                ease: "linear",
              }}
            />
            <motion.div
              className={styles.ringInner}
              animate={{
                rotate: -360,
              }}
              transition={{
                duration: 1,
                repeat: Infinity,
                ease: "linear",
              }}
            />
          </div>
        );
      
      case "ripple":
        return (
          <div className={styles.rippleContainer}>
            {[0, 1].map((i) => (
              <motion.div
                key={i}
                className={styles.ripple}
                animate={{
                  scale: [1, 1.5],
                  opacity: [1, 0],
                }}
                transition={{
                  duration: 1.5,
                  repeat: Infinity,
                  delay: i * 0.75,
                  ease: "easeOut",
                }}
              />
            ))}
          </div>
        );
      
      case "pulse":
      default:
        return (
          <motion.div
            className={styles.pulse}
            animate={{
              scale: [0.8, 1.2, 0.8],
              opacity: [0.5, 1, 0.5],
            }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />
        );
    }
  };

  return (
    <div 
      className={spinnerClasses}
      role="status"
      aria-label={getAriaLabel()}
      aria-live="polite"
    >
      {renderSpinner()}
      {label && <span className={styles.srOnly}>{label}</span>}
    </div>
  );
};

export default Spinner;