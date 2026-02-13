import { Variants } from 'framer-motion';

/**
 * Comprehensive animation variants for consistent motion patterns
 * Eliminates repeated animation definitions across components
 */
export const AnimationVariants = {
  // Page transitions (used in HomePage, AboutPage, GenresPage, etc.)
  page: {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.5, ease: "easeOut" }
  } as Variants,

  // Section transitions (used for content sections)
  section: {
    initial: { opacity: 0, y: 30 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6, ease: "easeOut" }
  } as Variants,

  // Card animations (used in FeatureCard, TechStackCard, StatCounter, etc.)
  card: {
    initial: { opacity: 0, y: 30 },
    animate: { opacity: 1, y: 0 },
    hover: { y: -8, scale: 1.02 },
    transition: { duration: 0.5, ease: "easeOut" }
  } as Variants,

  // Movie/Genre card specific animations
  movieCard: {
    whileHover: { y: -6, scale: 1.02 },
    whileTap: { scale: 0.98, y: -3 },
    transition: { duration: 0.2, ease: [0.4, 0, 0.2, 1] as [number, number, number, number] }
  },

  // Button animations (used in multiple components)
  button: {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    hover: { y: -3, boxShadow: "var(--shadow-xl)" },
    tap: { y: -1, boxShadow: "var(--shadow-lg)" },
    transition: { duration: 0.2 }
  } as Variants,

  // Image hover animations
  image: {
    whileHover: { scale: 1.08, filter: "brightness(1.05)" },
    transition: { duration: 0.3, ease: [0.4, 0, 0.2, 1] }
  },

  // Badge animations
  badge: {
    whileHover: { scale: 1.05 },
    whileTap: { scale: 0.95 },
    transition: { duration: 0.2 }
  },

  // Staggered list animations
  stagger: {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { 
        staggerChildren: 0.1, 
        delayChildren: 0.2 
      }
    }
  } as Variants,

  // Staggered container for list items
  staggerContainer: {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2
      }
    }
  } as Variants,

  // Individual staggered item
  staggerItem: {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  } as Variants,

  // Fade animations
  fade: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    exit: { opacity: 0 },
    transition: { duration: 0.3 }
  } as Variants,

  // Slide animations
  slide: {
    initial: { x: -20, opacity: 0 },
    animate: { x: 0, opacity: 1 },
    exit: { x: 20, opacity: 0 },
    transition: { duration: 0.3 }
  } as Variants,

  // Scale animations
  scale: {
    initial: { scale: 0.8, opacity: 0 },
    animate: { scale: 1, opacity: 1 },
    exit: { scale: 0.8, opacity: 0 },
    transition: { duration: 0.3 }
  } as Variants,

  // Navigation animations
  navItem: {
    initial: { opacity: 0, y: -10 },
    animate: { opacity: 1, y: 0 },
    hover: { y: -2 },
    transition: { duration: 0.2 }
  } as Variants,

  // Loading animations
  loading: {
    initial: { opacity: 0 },
    animate: { opacity: 1 },
    exit: { opacity: 0 }
  } as Variants,

  // Error animations
  error: {
    initial: { opacity: 0, x: -10 },
    animate: { opacity: 1, x: 0 },
    transition: { duration: 0.3 }
  } as Variants,

  // Success animations
  success: {
    initial: { scale: 0.8, opacity: 0 },
    animate: { scale: 1, opacity: 1 },
    transition: { 
      duration: 0.5, 
      ease: "easeOut",
      type: "spring"
    }
  } as Variants
};

/**
 * Helper function to get animation props with delay
 * Useful for staggered animations
 */
export const getAnimationProps = (variant: keyof typeof AnimationVariants, delay?: number) => {
  const animation = AnimationVariants[variant];
  
  if (delay && typeof animation === 'object' && 'animate' in animation && animation.animate && 'transition' in animation.animate) {
    return {
      ...animation,
      animate: {
        ...animation.animate,
        transition: {
          ...(animation.animate as any).transition,
          delay
        }
      }
    };
  }
  
  return animation;
};

/**
 * Helper function to create staggered animation variants
 * For lists with dynamic number of items
 */
export const createStaggeredVariants = (baseVariant: Variants, staggerDelay: number = 0.1) => ({
  container: {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: staggerDelay,
        delayChildren: 0.2
      }
    }
  },
  item: baseVariant
});

export default AnimationVariants;