import React from "react";
import { motion, Variants } from "framer-motion";

import styles from "../../styles/components/pages/HomePage.module.css";

const HomePage: React.FC = () => {
  // Motion variants for page animations
  const pageVariants: Variants = {
    initial: { opacity: 0, y: 20 },
    animate: {
      opacity: 1,
      y: 0
    }
  };

  const sectionVariants: Variants = {
    initial: { opacity: 0, y: 30 },
    animate: {
      opacity: 1,
      y: 0
    }
  };

  const featureVariants: Variants = {
    initial: { opacity: 0, scale: 0.9 },
    animate: {
      opacity: 1,
      scale: 1
    },
    hover: {
      y: -8,
      scale: 1.02
    }
  };

  const buttonVariants: Variants = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    hover: {
      y: -3,
      boxShadow: "var(--shadow-xl)"
    },
    tap: {
      y: -1,
      boxShadow: "var(--shadow-lg)"
    }
  };

  const features = [
    {
      icon: "Films",
      title: "Extensive Collection",
      description: "Discover thousands of movies across all genres and decades"
    },
    {
      icon: "Rating",
      title: "Curated Ratings", 
      description: "IMDb and Rotten Tomatoes ratings to help you choose"
    },
    {
      icon: "Search",
      title: "Smart Search",
      description: "Find exactly what you're looking for with powerful filters"
    }
  ];
  return (
    <motion.div
      className={styles.homePageContainer}
      variants={pageVariants}
      initial="initial"
      animate="animate"
      transition={{ duration: 0.6, ease: "easeOut", staggerChildren: 0.2 }}
    >
      <motion.section
        className={styles.heroSection}
        variants={sectionVariants}
        transition={{ duration: 0.5, ease: "easeOut" }}
      >
        <h1 className={styles.heroTitle}>Welcome to MovieDB</h1>
        <p className={styles.heroSubtitle}>
          Explore our curated collection of movies from MongoDB sample_mflix
          dataset
        </p>
        <div className={styles.heroActions}>
          <motion.a
            variants={buttonVariants}
            initial="initial"
            animate="animate"
            whileHover="hover"
            whileTap="tap"
            href="/movies"
            className={styles.btnPrimary}
          >
            Browse Movies
          </motion.a>
          <motion.a
            variants={buttonVariants}
            initial="initial"
            animate="animate"
            whileHover="hover"
            whileTap="tap"
            href="/top-rated"
            className={styles.btnSecondary}
          >
            Top Rated
          </motion.a>
        </div>
      </motion.section>

      <motion.section
        className={styles.featuresGrid}
        variants={sectionVariants}
      >
        {features.map((feature, index) => (
          <motion.div
            key={index}
            className={`${styles.featureCard} card-hover`}
            variants={featureVariants}
            transition={{ 
              duration: 0.5, 
              ease: "easeOut", 
              delay: index * 0.1 
            }}
            whileHover="hover"
          >
            <div className={styles.featureIcon}>{feature.icon}</div>
            <h3>{feature.title}</h3>
            <p>{feature.description}</p>
          </motion.div>
        ))}
      </motion.section>
    </motion.div>
  );
};

export default HomePage;
