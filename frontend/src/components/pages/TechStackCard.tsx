import React from "react";
import { motion, Variants } from "framer-motion";
import styles from "../../styles/components/pages/AboutPage.module.css";

interface TechStackCardProps {
  name: string;
  category: string;
  description: string;
  color: string;
  index: number;
}

const TechStackCard: React.FC<TechStackCardProps> = ({
  name,
  category,
  description,
  color,
  index
}) => {
  const cardVariants: Variants = {
    initial: { opacity: 0, scale: 0.9 },
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
      className={styles.techStackCard}
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
      <div
        className={styles.techStackIcon}
        style={{ backgroundColor: color }}
      >
        <span className={styles.techStackInitial}>
          {name.charAt(0)}
        </span>
      </div>
      <div className={styles.techStackContent}>
        <h3 className={styles.techStackName}>{name}</h3>
        <span className={styles.techStackCategory}>{category}</span>
        <p className={styles.techStackDescription}>{description}</p>
      </div>
    </motion.div>
  );
};

export default TechStackCard;
