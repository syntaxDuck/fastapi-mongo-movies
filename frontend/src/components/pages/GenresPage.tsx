import React, { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import { Movie } from "../../types";
import { movieService } from "../../services/api";
import styles from "../../styles/components/pages/GenresPage.module.css";
import GenreCard from "../genres/GenreCard";
import { LoadingWrapper, LoadingSpinners } from "../ui/LoadingComponents";

const GenresPage: React.FC = () => {
  const [genres, setGenres] = useState<{ genre: string; movie: Movie }[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [initialLoad, setInitialLoad] = useState(true);

  const loadGenres = useCallback(async () => {
    try {
      setLoading(true);
      const genre_types = await movieService.getMovieGenres();

      // ⚡ Bolt: Parallelize API calls to fetch genre sample movies
      // This reduces load time from O(N) to O(1) relative to number of genres
      const genreMoviesPromises = genre_types.map(async (genre) => {
        try {
          // ⚡ Bolt: Reduced limit from 25 to 5 to minimize payload size
          const movie_batch = await movieService.getMovieByGenre(genre, {
            limit: 5,
          });
          return { genre, movie_batch };
        } catch (e) {
          console.warn(`Failed to load movies for genre ${genre}:`, e);
          return { genre, movie_batch: [] };
        }
      });

      const results = await Promise.all(genreMoviesPromises);

      // ⚡ Bolt: Post-fetch uniqueness check to ensure distinct posters
      const usedMovieIds = new Set<string>();
      const finalGenres: { genre: string; movie: Movie }[] = [];

      for (const { genre, movie_batch } of results) {
        // Try to find a movie not already used as a poster for another genre
        const uniqueMovie = movie_batch.find((m) => !usedMovieIds.has(m._id));

        // Only add the genre if we found a unique candidate, preserving the uniqueness invariant
        if (uniqueMovie) {
          usedMovieIds.add(uniqueMovie._id);
          finalGenres.push({ genre, movie: uniqueMovie });
        } else {
          console.debug(
            `Skipping genre ${genre} - no unique poster available in batch`,
          );
        }
      }

      setGenres(finalGenres);
      setError(null);
      setInitialLoad(false);
    } catch (err) {
      setError("Failed to load genres");
      console.error("Error loading genres:", err);
      setInitialLoad(false);
    } finally {
      setLoading(false);
    }
  }, []);

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
      <div className={styles.genresPageContainer}>
        <motion.div
          className={styles.genresHeader}
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className={styles.genresTitle}>Movie Genres</h1>
          <p className={styles.genresSubtitle}>
            Explore our collection by genre
          </p>
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
                    <LoadingSpinners.Default
                      size="sm"
                      color="gray"
                      type="dots"
                    />
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
      <div className={styles.genresPageContainer}>
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
    <div className={styles.genresPageContainer}>
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

export default GenresPage;
