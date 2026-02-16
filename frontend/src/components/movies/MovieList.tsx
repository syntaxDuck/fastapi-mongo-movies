import React, { useEffect, useCallback, useMemo, memo } from "react";
import { useSearchParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Movie } from "../../types";
import { FilterBuilder, MovieFilters } from "../../utils/filterBuilder";
import styles from "../../styles/components/movies/MovieList.module.css";
import MovieCard from "./MovieCard";
import { LoadingWrapper, LoadingSpinners } from "../ui/LoadingComponents";
import { useMovies } from "../../hooks";

interface MovieListProps {
  filter?: MovieFilters;
  onMovieSelect?: (movieId: string) => void;
  disableCardLink?: boolean;
}

const listContainerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2,
    },
  },
};

const MovieList: React.FC<MovieListProps> = memo(({ filter, onMovieSelect = null, disableCardLink = false }) => {
  const [searchParams] = useSearchParams();
  const searchQuery = searchParams.get("search");

  const queryParams = {
    ...filter,
    ...(searchQuery && { search: searchQuery }),
  };

  const {
    data,
    isLoading,
    error,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
  } = useMovies(queryParams);

  const movies = useMemo(() => data?.pages.flat() ?? [], [data?.pages]);

  const handleMovieClick = useCallback((movieId: string) => {
    if (onMovieSelect) {
      onMovieSelect(movieId);
    }
  }, [onMovieSelect]);

  const handleLoadMore = useCallback(() => {
    fetchNextPage();
  }, [fetchNextPage]);

  useEffect(() => {
    if (error) {
      console.error("Error loading movies:", error);
    }
  }, [error]);

  if (isLoading) {
    return (
      <div className={styles.movieListContainer}>
        <LoadingWrapper
          isLoading={true}
          children={null}
          fallback={
            <div className={styles.movieList}>
              {Array.from({ length: 6 }, (_, i) => (
                <div key={`skeleton-${i}`} className={styles.movie} role="status" aria-label={`Loading movie ${i + 1}`}>
                  <div className={styles.skeletonPoster}>
                    <LoadingSpinners.Default size="sm" color="gray" type="dots" />
                  </div>
                </div>
              ))}
            </div>
          }
        />
      </div>
    );
  }

  if (error) {
    return <div className={styles.error}>Failed to load movies</div>;
  }

  return (
    <div className={styles.movieListContainer}>
      <motion.div
        className={styles.movieList}
        layout
        initial="hidden"
        animate="visible"
        variants={listContainerVariants}
      >
        <AnimatePresence mode="popLayout">
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
            >
              <MovieCard
                onMovieClick={handleMovieClick}
                movie={movie}
                disableLink={disableCardLink}
              />
            </motion.div>
          ))}
        </AnimatePresence>
      </motion.div>

      {hasNextPage && (
        <div className={styles.loadMoreContainer}>
          <button
            onClick={handleLoadMore}
            disabled={isFetchingNextPage}
            className={styles.loadMoreBtn}
            aria-busy={isFetchingNextPage}
          >
            {isFetchingNextPage ? (
              <div className="flex items-center gap-2">
                <LoadingSpinners.Inline size="sm" color="white" type="dots" />
                <span>Loading...</span>
              </div>
            ) : (
              "Load More Movies ▷"
            )}
          </button>
        </div>
      )}

      {!hasNextPage && movies.length > 0 && (
        <div className={styles.noMore}>
          <p>You've reached the end!</p>
          <p>No more movies to load</p>
        </div>
      )}
    </div>
  );
});

MovieList.displayName = "MovieList";

export default MovieList;
