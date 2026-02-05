import React, { useState, useEffect, useCallback } from "react";
import { Movie } from "../../types";
import { movieService } from "../../services/api";
import styles from "../../styles/components/movies/MovieList.module.css";
import GenreCard from "./GenreCard";

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
        const genres: { genre: string, movie: Movie }[] = [];

        for (const genre of genre_types) {
          try {
            const movie_batch: Movie[] = (await movieService.getMovieByGenre(genre, { limit: 25 }));

            for (const movie of movie_batch) {
              const found = genres.find((genre) => movie._id === genre.movie._id);

              if (!found) {
                genres.push({ genre, movie: movie });
                break
              }
            }

          } catch (e) {
            console.warn(`Failed to load movies for genre ${genre}:`, e);
            continue;
          }
        }

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


  if (initialLoad && loading) {
    return (
      <div className={styles.movieListContainer}>
        <div className={styles.movieList}>
          {Array.from({ length: 6 }, (_, i) => (
            <GenreCard key={`skeleton-${i}`} />
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
          <GenreCard key={`${genre.movie._id}-${index}`} genre={genre.genre} movie={genre.movie} />
        ))}
      </div>
    </div>
  );
};

export default GenreList;
