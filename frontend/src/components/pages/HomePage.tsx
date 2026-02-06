import React from "react";
import {
  NavLink,
} from "react-router-dom";

import styles from "../../styles/components/pages/HomePage.module.css";

const HomePage: React.FC = () => {
  return (
    <div className={`${styles.homePageContainer} fade-in`}>
      <div className={styles.heroSection}>
        <h1 className={styles.heroTitle}>Welcome to MovieDB</h1>
        <p className={styles.heroSubtitle}>
          Explore our curated collection of movies from the MongoDB sample_mflix
          dataset
        </p>
        <div className={styles.heroActions}>
          <NavLink
            to="/movies"
            className={`${styles.btnPrimary} btn-hover-lift`}
          >
            Browse Movies
          </NavLink>
          <NavLink
            to="/top-rated"
            className={`${styles.btnSecondary} btn-hover-lift`}
          >
            Top Rated
          </NavLink>
        </div>
      </div>

      <div className={styles.featuresGrid}>
        <div className={`${styles.featureCard} card-hover`}>
          <div className={styles.featureIcon}>Films</div>
          <h3>Extensive Collection</h3>
          <p>Discover thousands of movies across all genres and decades</p>
        </div>
        <div className={`${styles.featureCard} card-hover`}>
          <div className={styles.featureIcon}>Rating</div>
          <h3>Curated Ratings</h3>
          <p>IMDb and Rotten Tomatoes ratings to help you choose</p>
        </div>
        <div className={`${styles.featureCard} card-hover`}>
          <div className={styles.featureIcon}>Search</div>
          <h3>Smart Search</h3>
          <p>Find exactly what you're looking for with powerful filters</p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
