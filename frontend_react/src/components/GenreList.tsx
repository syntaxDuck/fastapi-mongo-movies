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

        const genres = await movieService.getMovieGenres();
        var genreCovers: { genre: string, movie: Movie }[] = []
        for (const genre of genres) {
          try {
            const movie = await movieService.getMovieByGenre(genre, { limit: 1 })
            console.log(movie)
          }
          catch {
          }

          // genreCovers.push({ genre: genre, movie: movie[0] })
        }


        if (reset) {
          setGenres(genreCovers)
        } else {
          setGenres((prev) => [...prev, ...genreCovers]);
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
    [],
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
        {/* {genres.map((genre, index) => ( */}
        {/*   <div key={`${genre._id}-${index}`} className={styles.genre}> */}
        {/*     <Link to={`/genre/${genre._id}`} className={styles.genreLink}> */}
        {/*       <img */}
        {/*         src={genre.poster} */}
        {/*         alt={genre.title} */}
        {/*         onError={handleImageError} */}
        {/*         className={styles.genrePoster} */}
        {/*         loading="lazy" */}
        {/*       /> */}
        {/*       <div className={styles.genreHoverText}>{genre.title}</div> */}
        {/*       {genre.year && ( */}
        {/*         <div className={styles.genreYear}>{genre.year}</div> */}
        {/*       )} */}
        {/*       {genre.imdb?.rating && ( */}
        {/*         <div className={styles.genreRating}>⭐ {genre.imdb.rating}</div> */}
        {/*       )} */}
        {/*     </Link> */}
        {/*   </div> */}
        {/* ))} */}
      </div>
    </div>
  );
};

export default GenreList;
