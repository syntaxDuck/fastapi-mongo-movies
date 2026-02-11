import React from "react";
import { motion } from "framer-motion";
import styles from "../../styles/components/ui/Badge.module.css";

export interface BadgeProps {
  /** Badge content */
  children: React.ReactNode;
  /** Badge variant for styling */
  variant?:
    | "default"
    | "success"
    | "warning"
    | "error"
    | "info"
    | "primary"
    | "secondary";
  /** Badge size */
  size?: "sm" | "md" | "lg";
  /** Badge position for absolute positioning */
  position?: "top-left" | "top-right" | "bottom-left" | "bottom-right";
  /** Additional CSS classes */
  className?: string;
  /** Animation type for interactions */
  animation?: "scale" | "fade" | "none";
  /** Badge shape */
  shape?: "rounded" | "pill" | "square";
  /** Badge style variant */
  style?: "solid" | "outlined";
  /** Icon to display before text */
  icon?: string;
  /** Whether badge is disabled */
  disabled?: boolean;
  /** Badge ID for accessibility */
  id?: string;
  /** ARIA label for accessibility */
  ariaLabel?: string;
}

const Badge: React.FC<BadgeProps> = ({
  children,
  variant = "default",
  size = "md",
  position,
  className = "",
  animation = "scale",
  shape = "rounded",
  style = "solid",
  icon,
  disabled = false,
  id,
  ariaLabel,
}) => {
  const badgeClasses = [
    styles.badge,
    styles["badge" + variant.charAt(0).toUpperCase() + variant.slice(1)],
    styles["badge" + size.charAt(0).toUpperCase() + size.slice(1)],
    position &&
      styles[
        "badge" +
          position
            .split("-")
            .map((s) => s.charAt(0).toUpperCase() + s.slice(1))
            .join("")
      ],
    shape !== "rounded" &&
      styles[`badge${shape.charAt(0).toUpperCase() + shape.slice(1)}`],
    style === "outlined" && styles.badgeOutlined,
    icon && styles.badgeIcon,
    disabled && styles.disabled,
    className,
  ]
    .filter(Boolean)
    .join(" ");

  const getAnimationProps = () => {
    if (animation === "none" || disabled) {
      return {};
    }

    switch (animation) {
      case "scale":
        return {
          whileHover: { scale: 1.05 },
          whileTap: { scale: 0.95 },
          transition: { duration: 0.2 } as any,
        };
      case "fade":
        return {
          whileHover: { opacity: 0.8 },
          transition: { duration: 0.2 } as any,
        };
      default:
        return {};
    }
  };

  const badgeContent = (
    <>
      {icon && <span className={styles.badgeIcon} data-icon={icon} />}
      {children}
    </>
  );

  return (
    <motion.div
      id={id}
      className={badgeClasses}
      aria-label={ariaLabel}
      {...getAnimationProps()}
    >
      {badgeContent}
    </motion.div>
  );
};

export default Badge;
