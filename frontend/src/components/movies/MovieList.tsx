import React, { useState, useEffect, useCallback } from "react";
import { useSearchParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Movie } from "../../types";
import { movieService } from "../../services/api";
import { FilterBuilder, MovieFilters } from "../../utils/filterBuilder";
import styles from "../../styles/components/movies/MovieList.module.css";
import MovieCard from "./MovieCard";
import { LoadingWrapper, LoadingSpinners } from "../ui/LoadingComponents";


interface MovieListProps {
  filter?: MovieFilters;
  onMovieSelect?: CallableFunction;
  disableCardLink?: boolean;
}

const MovieList: React.FC<MovieListProps> = ({ filter, onMovieSelect = null, disableCardLink = false }) => {
  const [searchParams] = useSearchParams();
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [initialLoad, setInitialLoad] = useState(true);

  const pageSize = 24;

  // Get search query from URL
  const searchQuery = searchParams.get("search");

  const loadMovies = useCallback(
    async (pageNum: number, reset = false) => {
      try {
        setLoading(true);
        
        // Build dynamic query parameters using FilterBuilder
        const queryParams = FilterBuilder.buildQueryParams(filter || {});
        
        // Add pagination parameters
        queryParams.skip = pageNum * pageSize;
        queryParams.limit = pageSize;
        
        // Add search query if present
        if (searchQuery) {
          queryParams.search = searchQuery;
        }
        
        // Default to movies only if type not specified
        if (!queryParams.type) {
          queryParams.type = "movie";
        }
        
        // Validate filters before making API call
        const validation = FilterBuilder.validateFilters(filter || {});
        if (!validation.isValid) {
          console.warn("Filter validation warnings:", validation.errors);
        }
        
        // Single API call to flexible endpoint
        const newMovies = await movieService.fetchMovies(queryParams);

        if (reset) {
          setMovies(newMovies);
        } else {
          setMovies((prev) => [...prev, ...newMovies]);
        }

        setHasMore(newMovies.length === pageSize);
        setError(null);
        setInitialLoad(false);
      } catch (err) {
        setError("Failed to load movies");
        console.error("Error loading movies:", err);
        setInitialLoad(false);
      } finally {
        setLoading(false);
      }
    },
    [filter, pageSize, searchQuery],
  );

  useEffect(() => {
    setPage(0);
    setInitialLoad(true);
    loadMovies(0, true);
  }, [filter, loadMovies]);

  const loadMore = () => {
    const nextPage = page + 1;
    setPage(nextPage);
    loadMovies(nextPage, false);
  };

  if (initialLoad && loading) {
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
    return <div className={styles.error}>{error}</div>;
  }

  return (
    <div className={styles.movieListContainer}>
      <motion.div
        className={styles.movieList}
        layout
        initial="hidden"
        animate="visible"
        variants={{
          hidden: { opacity: 0 },
          visible: {
            opacity: 1,
            transition: {
              staggerChildren: 0.1,
              delayChildren: 0.2,
            },
          },
        }}
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
              whileHover={{
                y: -6,
                scale: 1.02,
                transition: { duration: 0.2 },
              }}
              whileTap={{ scale: 0.98 }}
            >
              <MovieCard
                onClick={() => onMovieSelect ? onMovieSelect(movie._id) : null}
                movie={movie}
                disableLink={disableCardLink}
              />
            </motion.div>
          ))}
        </AnimatePresence>
      </motion.div>

      {hasMore && (
        <div className={styles.loadMoreContainer}>
          <button
            onClick={loadMore}
            disabled={loading}
            className={styles.loadMoreBtn}
            aria-busy={loading}
          >
            {loading ? (
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

      {!hasMore && movies.length > 0 && (
        <div className={styles.noMore}>
          <p>You've reached the end!</p>
          <p>No more movies to load</p>
        </div>
      )}
    </div>
  );
};

export default MovieList;
