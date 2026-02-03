import React, { useState, useEffect, useCallback } from "react";
import { Link } from "react-router-dom";
import { Movie } from "../types";
import { movieService } from "../services/api";
import styles from "../styles/components/MovieList.module.css";

const GenreList: React.FC = () => {
  const [genres, setGenres] = useState<{ genre: string, movie: Movie }[]>([])
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [initialLoad, setInitialLoad] = useState(true);

  const loadGenres = useCallback(
    async (reset = false) => {
      try {

        setLoading(true);
        const genre_types = await movieService.getMovieGenres();
        const movies: Movie[] = [];
        for (const genre of genre_types) {
          try {
            const movie_batch: Movie[] = (await movieService.getMovieByGenre(genre, { limit: 5 }))

            for (const movie of movie_batch) {
              try {


                const movie_exists = movies.some(item => {
                  return item._id === movie._id
                });

                //TODO: Kind of a patch right now, should probably verify these poster links on the backend
                const valid_poster = await new Promise((resolve) => {
                  const img = new Image();
                  img.onload = () => resolve(true); // Image loaded successfully
                  img.onerror = () => resolve(false); // Image failed to load (404, invalid format, etc.)
                  img.src = movie.poster;
                });

                if (!movie_exists && valid_poster)
                  movies.push(movie);

              } catch (e) {
                continue
              }
            }
          } catch { }
        }

        const genres: { genre: string, movie: Movie }[] = genre_types.map((key, index) => {
          return { genre: key, movie: movies[index] };
        })

        if (reset) {
          setGenres(prev =>
            reset ? genres : [...prev, ...genres]
          );
        } else {
          setGenres((prev) => [...prev, ...genres]);
        }

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
    []
  );

  useEffect(() => {
    setInitialLoad(true);
    loadGenres(true);
  }, [loadGenres]);

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
        {genres.map((genre, index) => (
          <div key={`${genre.genre}-${index}`} className={styles.movie}>
            <Link to={`/genre/${genre.genre}`} className={styles.movieLink}>
              <img
                src={genre.movie.poster}
                alt={genre.movie.title}
                onError={handleImageError}
                className={styles.moviePoster}
                loading="lazy"
              />
              <div className={styles.movieHoverText}>{genre.movie.title}</div>
              {genre.movie.year && (
                <div className={styles.movieYear}>{genre.movie.year}</div>
              )}
              {genre.movie.imdb?.rating && (
                <div className={styles.movieRating}>⭐ {genre.movie.imdb?.rating}</div>
              )}
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default GenreList;
