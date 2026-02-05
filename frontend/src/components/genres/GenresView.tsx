import React, { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import { Movie } from "../../types";
import { movieService } from "../../services/api";
import styles from "../../styles/components/genres/GenresView.module.css";
import GenreCard from "./GenreCard";
import { LoadingWrapper, LoadingSpinners } from "../ui/LoadingComponents";

const GenresView: React.FC = () => {
  const [genres, setGenres] = useState<{ genre: string, movie: Movie }[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [initialLoad, setInitialLoad] = useState(true);

  const loadGenres = useCallback(
    async () => {
      try {
        setLoading(true);
        const genre_types = await movieService.getMovieGenres();
        const genres: { genre: string, movie: Movie }[] = [];

        for (const genre of genre_types) {
          try {
            const movie_batch: Movie[] = (await movieService.getMovieByGenre(genre, { limit: 25 }));

            for (const movie of movie_batch) {
              const found = genres.find((g) => movie._id === g.movie._id);

              if (!found) {
                genres.push({ genre, movie: movie });
                break;
              }
            }

          } catch (e) {
            console.warn(`Failed to load movies for genre ${genre}:`, e);
            continue;
          }
        }

        setGenres(genres);
        setError(null);
        setInitialLoad(false);
      } catch (err) {
        setError("Failed to load genres");
        console.error("Error loading genres:", err);
        setInitialLoad(false);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  useEffect(() => {
    setInitialLoad(true);
    loadGenres();
  }, [loadGenres]);

  // Animation variants for genre cards
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0 },
  };

  if (initialLoad && loading) {
    return (
      <div className={styles.genresViewContainer}>
        <motion.div 
          className={styles.genresHeader}
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className={styles.genresTitle}>Movie Genres</h1>
          <p className={styles.genresSubtitle}>Explore our collection by genre</p>
        </motion.div>
        
        <LoadingWrapper 
          isLoading={true} 
          children={null}
          fallback={
            <motion.div 
              className={styles.genresGrid}
              variants={containerVariants}
              initial="hidden"
              animate="visible"
            >
              {Array.from({ length: 12 }, (_, i) => (
                <motion.div
                  key={`skeleton-${i}`}
                  className={styles.genreCardSkeleton}
                  variants={cardVariants}
                  role="status"
                  aria-label={`Loading genre ${i + 1}`}
                >
                  <div className={styles.skeletonPoster}>
                    <LoadingSpinners.Default size="sm" color="gray" type="dots" />
                  </div>
                  <div className={styles.skeletonTitle}></div>
                </motion.div>
              ))}
            </motion.div>
          } 
        />
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.genresViewContainer}>
        <motion.div 
          className={styles.errorContainer}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
        >
          <div className={styles.errorIcon}>⚠️</div>
          <h2>Oops! Something went wrong</h2>
          <p>{error}</p>
          <motion.button
            className={styles.retryButton}
            onClick={loadGenres}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Try Again
          </motion.button>
        </motion.div>
      </div>
    );
  }

  return (
    <div className={styles.genresViewContainer}>
      <motion.div 
        className={styles.genresHeader}
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className={styles.genresTitle}>Movie Genres</h1>
        <p className={styles.genresSubtitle}>
          Discover {genres.length} different genres from our collection
        </p>
      </motion.div>

      <motion.div 
        className={styles.genresGrid}
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {genres.map((genre, index) => (
          <motion.div
            key={`${genre.genre}-${index}`}
            variants={cardVariants}
            whileHover={{ y: -8, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            transition={{ duration: 0.2 }}
          >
            <GenreCard genre={genre.genre} movie={genre.movie} />
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
};

export default GenresView;