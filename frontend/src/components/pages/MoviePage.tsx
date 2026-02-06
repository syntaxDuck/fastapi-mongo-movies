import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import MovieDetails from "../movies/MovieDetails";
import MovieList from "../movies/MovieList";
import styles from "../../styles/components/pages/MoviePage.module.css";

function useMediaQuery(query: string) {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    if (media.matches !== matches) {
      setMatches(media.matches);
    }

    const listener = () => setMatches(media.matches);
    media.addEventListener('change', listener);

    return () => media.removeEventListener('change', listener);
  }, [matches, query]);

  return matches;
}

const MoviePage: React.FC = () => {
  const [selectedMovie, setSelectedMovie] = useState("");

  const handleMovieSelect = (movieId: string) => {
    setSelectedMovie(movieId)
  }

  const isDesktop = useMediaQuery('(min-width: 1025px)');

  return (
    <div className={styles.moviePageContainer}>
      <MovieList onMovieSelect={handleMovieSelect} />
      {isDesktop && (
        <div className={styles.movieDetailsContainer}>
          {selectedMovie ? (
            <MovieDetails id={selectedMovie} />
          ) : (
            <motion.div
              className={styles.selectMoviePrompt}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, ease: [0.4, 0, 0.2, 1] }}
            >
              <div className={styles.promptIcon}>🎬</div>
              <h2 className={styles.promptTitle}>Select a Movie</h2>
              <p className={styles.promptText}>
                Choose a movie from the list to view its details, ratings, and additional information.
              </p>
              <div className={styles.promptFeatures}>
                <div className={styles.feature}>
                  <span className={styles.featureIcon}>⭐</span>
                  <span className={styles.featureText}>Page Ratings</span>
                </div>
                <div className={styles.feature}>
                  <span className={styles.featureIcon}>📽️</span>
                  <span className={styles.featureText}>Movie Details</span>
                </div>
                <div className={styles.feature}>
                  <span className={styles.featureIcon}>🎭</span>
                  <span className={styles.featureText}>Cast & Crew</span>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      )}
    </div>
  );
}

export default MoviePage
