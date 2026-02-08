import React, { useEffect, useState } from "react";
import { motion, Variants } from "framer-motion";
import styles from "../../styles/components/pages/AboutPage.module.css";

interface StatCounterProps {
  number: number;
  label: string;
  suffix: string;
  index: number;
}

const StatCounter: React.FC<StatCounterProps> = ({ number, label, suffix, index }) => {
  const [count, setCount] = useState(0);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Start counting when component comes into view
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, index * 200); // Stagger the animations

    return () => clearTimeout(timer);
  }, [index]);

  useEffect(() => {
    if (!isVisible) return;

    const duration = 2000; // 2 seconds for the animation
    const steps = 60; // Number of steps in the animation
    const increment = number / steps;
    let currentCount = 0;

    const counter = setInterval(() => {
      currentCount += increment;
      if (currentCount >= number) {
        setCount(number);
        clearInterval(counter);
      } else {
        setCount(Math.floor(currentCount));
      }
    }, duration / steps);

    return () => clearInterval(counter);
  }, [isVisible, number]);

  const cardVariants: Variants = {
    initial: { opacity: 0, scale: 0.8 },
    animate: {
      opacity: 1,
      scale: 1
    },
    hover: {
      scale: 1.05
    }
  };

  return (
    <motion.div
      className={styles.statCard}
      variants={cardVariants}
      initial="initial"
      animate="animate"
      whileHover="hover"
      transition={{ 
        duration: 0.5, 
        ease: "easeOut", 
        delay: index * 0.1 
      }}
    >
      <div className={styles.statNumber}>
        {count}{suffix}
      </div>
      <div className={styles.statLabel}>
        {label}
      </div>
    </motion.div>
  );
};

export default StatCounter;
