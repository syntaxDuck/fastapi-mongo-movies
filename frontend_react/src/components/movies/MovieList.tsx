import React, { useState, useEffect, useCallback } from "react";
import { useSearchParams } from "react-router-dom";
import { Movie } from "../../types";
import { movieService } from "../../services/api";
import styles from "../../styles/components/movies/MovieList.module.css";
import MovieCard from "./MovieCard";
import MovieDetails from "./MovieDetails";

interface MovieListProps {
  filter?: {
    genre?: string;
    director?: string;
    minYear?: number;
    maxYear?: number;
    minRating?: number;
  };
}

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

const MovieList: React.FC<MovieListProps> = ({ filter }) => {
  const [searchParams] = useSearchParams();
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [initialLoad, setInitialLoad] = useState(true);

  const pageSize = 24;
  const isDesktop = useMediaQuery('(min-width: 1025px)');

  // Get search query from URL
  const searchQuery = searchParams.get("search");

  const loadMovies = useCallback(
    async (pageNum: number, reset = false) => {
      try {
        setLoading(true);
        const params = {
          type: "movie",
          skip: pageNum * pageSize,
          limit: pageSize,
          search: searchQuery || undefined,
          ...filter,
        };

        const newMovies = await movieService.fetchMovies(params);

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
        <div className={styles.movieList}>
          {Array.from({ length: 6 }, (_, i) => (
            <MovieCard key={`skeleton-${i}`} />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  return (
    <div className={styles.movieListContainer}>
      <div className={styles.movieList}>
        {movies.map((movie, index) => (
          <MovieCard key={`${movie._id}-${index}`} movie={movie} />
        ))}
      </div>

      {hasMore && (
        <div className={styles.loadMoreContainer}>
          <button
            onClick={loadMore}
            disabled={loading}
            className={styles.loadMoreBtn}
          >
            {loading ? "Loading..." : "Load More Movies ▷"}
          </button>
        </div>
      )}

      {!hasMore && movies.length > 0 && (
        <div className={styles.noMore}>
          <p>You've reached the end!</p>
          <p>No more movies to load</p>
        </div>
      )}

      {isDesktop && (
        <MovieDetails />
      )}
    </div>
  );
};

export default MovieList;
