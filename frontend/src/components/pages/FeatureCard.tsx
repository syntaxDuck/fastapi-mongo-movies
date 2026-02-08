import React from "react";
import { motion, Variants } from "framer-motion";
import styles from "../../styles/components/pages/AboutPage.module.css";

interface FeatureCardProps {
  icon: string;
  title: string;
  description: string;
  index: number;
}

const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description, index }) => {
  const cardVariants: Variants = {
    initial: { opacity: 0, y: 30 },
    animate: {
      opacity: 1,
      y: 0
    },
    hover: {
      y: -8,
      scale: 1.02
    }
  };

  return (
    <motion.div
      className={styles.featureCard}
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
      <div className={styles.featureIcon}>
        <span className={styles.featureIconEmoji}>{icon}</span>
      </div>
      <h3 className={styles.featureTitle}>{title}</h3>
      <p className={styles.featureDescription}>{description}</p>
    </motion.div>
  );
};

export default FeatureCard;
