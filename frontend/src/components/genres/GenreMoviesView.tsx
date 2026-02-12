import React, { useState, useEffect, useCallback } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Movie } from "../../types";
import { movieService } from "../../services/api";
import styles from "../../styles/components/genres/GenreMoviesView.module.css";
import MovieCard from "../movies/MovieCard";
import { LoadingWrapper, LoadingSpinners } from "../ui/LoadingComponents";

const PAGE_SIZE = 24;

const GenreMoviesView: React.FC = () => {
  const { genre } = useParams<{ genre: string }>();
  const navigate = useNavigate();
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [initialLoad, setInitialLoad] = useState(true);

  const loadMovies = useCallback(
    async (pageNum: number, reset = false) => {
      if (!genre) return;

      try {
        setLoading(true);
        const params = {
          limit: PAGE_SIZE,
          skip: pageNum * PAGE_SIZE,
        };

        const newMovies = await movieService.getMovieByGenre(genre, params);

        if (reset) {
          setMovies(newMovies);
        } else {
          setMovies((prev) => [...prev, ...newMovies]);
        }

        setHasMore(newMovies.length === PAGE_SIZE);
        setError(null);
        setInitialLoad(false);
      } catch (err) {
        setError(`Failed to load ${genre} movies`);
        console.error("Error loading genre movies:", err);
        setInitialLoad(false);
      } finally {
        setLoading(false);
      }
    },
    [genre]
  );

  useEffect(() => {
    if (genre) {
      setPage(0);
      setInitialLoad(true);
      loadMovies(0, true);
    }
  }, [genre, loadMovies]);

  const loadMore = useCallback(() => {
    const nextPage = page + 1;
    setPage(nextPage);
    loadMovies(nextPage, false);
  }, [page, loadMovies]);

  const goBack = () => {
    navigate("/genres");
  };

  // Animation variants
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
      <div className={styles.genreMoviesViewContainer}>
        <motion.div 
          className={styles.genreHeader}
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <motion.button
            className={styles.backButton}
            onClick={goBack}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            ← Back to Genres
          </motion.button>
          <h1 className={styles.genreTitle}>{genre}</h1>
          <p className={styles.genreSubtitle}>Loading movies...</p>
        </motion.div>

        <LoadingWrapper 
          isLoading={true} 
          children={null}
          fallback={
            <motion.div 
              className={styles.moviesGrid}
              variants={containerVariants}
              initial="hidden"
              animate="visible"
            >
              {Array.from({ length: 12 }, (_, i) => (
                <motion.div
                  key={`skeleton-${i}`}
                  className={styles.movieCardSkeleton}
                  variants={cardVariants}
                  role="status"
                  aria-label={`Loading movie ${i + 1}`}
                >
                  <div className={styles.skeletonPoster}>
                    <LoadingSpinners.Default size="sm" color="gray" type="dots" />
                  </div>
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
      <div className={styles.genreMoviesViewContainer}>
        <motion.div 
          className={styles.errorContainer}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
        >
          <motion.button
            className={styles.backButton}
            onClick={goBack}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            ← Back to Genres
          </motion.button>
          <div className={styles.errorIcon}>⚠️</div>
          <h2>Oops! Something went wrong</h2>
          <p>{error}</p>
          <motion.button
            className={styles.retryButton}
            onClick={() => loadMovies(0, true)}
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
    <div className={styles.genreMoviesViewContainer}>
      <motion.div 
        className={styles.genreHeader}
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <motion.button
          className={styles.backButton}
          onClick={goBack}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          ← Back to Genres
        </motion.button>
        <h1 className={styles.genreTitle}>{genre}</h1>
      </motion.div>

      <AnimatePresence mode="popLayout">
        <motion.div 
          className={styles.moviesGrid}
          layout
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          {movies.map((movie, index) => (
            <motion.div
              key={`${movie._id}-${index}`}
              layout
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -30 }}
              transition={{
                duration: 0.5,
                ease: [0.4, 0, 0.2, 1],
                delay: index * 0.05,
              }}
              whileHover={{ y: -6, scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              <MovieCard movie={movie} disableLink={false} />
            </motion.div>
          ))}
        </motion.div>
      </AnimatePresence>

      {hasMore && movies.length > 0 && (
        <motion.div 
          className={styles.loadMoreContainer}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <motion.button
            onClick={loadMore}
            disabled={loading}
            className={styles.loadMoreBtn}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            {loading ? (
              <div className="flex items-center gap-2">
                <LoadingSpinners.Inline size="sm" color="white" type="dots" />
                <span>Loading...</span>
              </div>
            ) : (
              "Load More Movies ▷"
            )}
          </motion.button>
        </motion.div>
      )}

      {!hasMore && movies.length > 0 && (
        <motion.div 
          className={styles.noMore}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <p>You've reached the end!</p>
          <p>No more {genre} movies to load</p>
        </motion.div>
      )}
    </div>
  );
};

export default GenreMoviesView;