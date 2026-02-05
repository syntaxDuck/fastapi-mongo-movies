import React from "react";
import {
  NavLink,
} from "react-router-dom";

import HomeStyles from "../styles/pages/Home.module.css";

const HeroPage: React.FC = () => {
  return (
    <div className="fade-in">
      <div className={HomeStyles.heroSection}>
        <h1 className={HomeStyles.heroTitle}>Welcome to MovieDB</h1>
        <p className={HomeStyles.heroSubtitle}>
          Explore our curated collection of movies from the MongoDB sample_mflix
          dataset
        </p>
        <div className={HomeStyles.heroActions}>
          <NavLink
            to="/movies"
            className={`${HomeStyles.btnPrimary} btn-hover-lift`}
          >
            Browse Movies
          </NavLink>
          <NavLink
            to="/top-rated"
            className={`${HomeStyles.btnSecondary} btn-hover-lift`}
          >
            Top Rated
          </NavLink>
        </div>
      </div>

      <div className={HomeStyles.featuresGrid}>
        <div className={`${HomeStyles.featureCard} card-hover`}>
          <div className={HomeStyles.featureIcon}>Films</div>
          <h3>Extensive Collection</h3>
          <p>Discover thousands of movies across all genres and decades</p>
        </div>
        <div className={`${HomeStyles.featureCard} card-hover`}>
          <div className={HomeStyles.featureIcon}>Rating</div>
          <h3>Curated Ratings</h3>
          <p>IMDb and Rotten Tomatoes ratings to help you choose</p>
        </div>
        <div className={`${HomeStyles.featureCard} card-hover`}>
          <div className={HomeStyles.featureIcon}>Search</div>
          <h3>Smart Search</h3>
          <p>Find exactly what you're looking for with powerful filters</p>
        </div>
      </div>
    </div>
  );
};

export default HeroPage;
