import React, { useState, useCallback } from "react";
import { motion } from "framer-motion";
import styles from "../../styles/components/ui/Image.module.css";
import { AnimationVariants } from "../../utils/animationVariants";

export interface ImageProps {
  /** Image source URL */
  src: string;
  /** Alt text for accessibility */
  alt: string;
  /** Fallback image URL on error */
  fallback?: string;
  /** Additional CSS classes */
  className?: string;
  /** Loading strategy */
  loading?: "lazy" | "eager";
  /** Aspect ratio (CSS value) */
  aspectRatio?: string;
  /** Animation type for interactions */
  animation?: "zoom" | "fade" | "slide" | "none";
  /** Custom error handler */
  onError?: (e: React.SyntheticEvent<HTMLImageElement>) => void;
  /** Image size preset */
  size?: "sm" | "md" | "lg" | "xl" | "auto";
  /** Border radius variant */
  rounded?: "none" | "sm" | "md" | "lg" | "xl" | "full";
  /** Object fit variant */
  objectFit?: "cover" | "contain" | "fill" | "scale-down" | "none";
  /** Shadow variant */
  shadow?: "none" | "sm" | "md" | "lg" | "xl";
  /** Image ID for accessibility */
  id?: string;
  /** Whether to show loading state */
  showLoading?: boolean;
}

const Image: React.FC<ImageProps> = ({
  src,
  alt,
  fallback = "https://thumbs.dreamstime.com/b/film-real-25021714.jpg",
  className = "",
  loading = "lazy",
  aspectRatio,
  animation = "zoom",
  onError,
  size,
  rounded = "lg",
  objectFit = "cover",
  shadow = "none",
  id,
  showLoading = true
}) => {
  const [imageState, setImageState] = useState<"loading" | "loaded" | "error">("loading");
  const [currentSrc, setCurrentSrc] = useState(src);

  const handleImageError = useCallback((e: React.SyntheticEvent<HTMLImageElement>) => {
    if (onError) {
      onError(e);
    } else {
      // Only use fallback if we haven't already tried it
      if (currentSrc !== fallback) {
        setCurrentSrc(fallback);
        setImageState("error");
      } else {
        setImageState("error");
      }
    }
  }, [onError, currentSrc, fallback]);

  const handleImageLoad = useCallback(() => {
    setImageState("loaded");
  }, []);

  const imageClasses = [
    styles.image,
    size && size !== "auto" && styles[`image${size.charAt(0).toUpperCase() + size.slice(1)}`],
    rounded && styles[`imageRounded${rounded.charAt(0).toUpperCase() + rounded.slice(1)}`],
    objectFit && styles[`image${objectFit.charAt(0).toUpperCase() + objectFit.slice(1)}`],
    shadow !== "none" && styles[`imageShadow${shadow === "md" ? "" : shadow.charAt(0).toUpperCase() + shadow.slice(1)}`],
    imageState === "loading" && showLoading && styles.loading,
    imageState === "error" && styles.error,
    className
  ].filter(Boolean).join(" ");

  const getAnimationProps = () => {
    if (animation === "none" || imageState === "error") {
      return {};
    }

    switch (animation) {
      case "zoom":
        return {
          whileHover: { scale: 1.08, filter: "brightness(1.05)" },
          transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] } as any
        };
      case "slide":
        return {
          whileHover: { x: 5 },
          transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] } as any
        };
      case "fade":
        return {
          initial: { opacity: 0 },
          animate: { opacity: 1 },
          whileHover: { opacity: 0.8 },
          transition: { duration: 0.3 } as any
        };
      default:
        return {};
    }
  };

  const imageStyle: React.CSSProperties = {
    aspectRatio
  };

  const animationProps = getAnimationProps();

  return (
    <motion.img
      id={id}
      src={currentSrc}
      alt={alt}
      onError={handleImageError}
      onLoad={handleImageLoad}
      className={imageClasses}
      loading={loading}
      style={imageStyle}
      {...animationProps}
      initial={animation !== "none" && animation === "fade" ? AnimationVariants.fade.initial as any : undefined}
      animate={imageState === "loaded" && animation !== "none" && animation === "fade" ? AnimationVariants.fade.animate as any : undefined}
    />
  );
};

export default Image;