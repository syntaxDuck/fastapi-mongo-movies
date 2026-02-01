import React, { useState, useEffect, useCallback } from "react";
import { Link } from "react-router-dom";
import { Movie } from "../types";
import { movieService } from "../services/api";
import styles from "../styles/components/MovieList.module.css";

interface MovieListProps {
  filter?: {
    genre?: string;
    director?: string;
    minYear?: number;
    maxYear?: number;
    minRating?: number;
  };
}

//TODO: Improve styleing 
//BUG: Unable to load more movies 
const MovieList: React.FC<MovieListProps> = ({ filter }) => {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [initialLoad, setInitialLoad] = useState(true);
  const pageSize = 20;

  const loadMovies = useCallback(
    async (pageNum: number, reset = false) => {
      try {
        setLoading(true);
        const params = {
          type: "movie",
          skip: pageNum * pageSize,
          limit: pageSize,
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
    [filter, pageSize],
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

  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>) => {
    e.currentTarget.src =
      "https://thumbs.dreamstime.com/b/film-real-25021714.jpg";
  };

  const MovieCardSkeleton: React.FC = () => (
    <div className={`${styles.movie} skeleton`}>
      <div className={styles.skeletonPoster}></div>
    </div>
  );

  if (initialLoad && loading) {
    return (
      <div className={styles.movieListContainer}>
        <div className={styles.movieList}>
          {Array.from({ length: 6 }, (_, i) => (
            <MovieCardSkeleton key={`skeleton-${i}`} />
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
          <div key={`${movie._id}-${index}`} className={styles.movie}>
            <Link to={`/movie/${movie._id}`} className={styles.movieLink}>
              <img
                src={movie.poster}
                alt={movie.title}
                onError={handleImageError}
                className={styles.moviePoster}
                loading="lazy"
              />
              <div className={styles.movieHoverText}>{movie.title}</div>
              {movie.year && (
                <div className={styles.movieYear}>{movie.year}</div>
              )}
              {movie.imdb?.rating && (
                <div className={styles.movieRating}>⭐ {movie.imdb.rating}</div>
              )}
            </Link>
          </div>
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
          <p>📽️ You've reached the end!</p>
          <p>No more movies to load</p>
        </div>
      )}
    </div>
  );
};

export default MovieList;
