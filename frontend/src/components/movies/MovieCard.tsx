import React from "react";
import { Link } from "react-router-dom";
import { Movie } from "../../types";
import styles from "../../styles/components/movies/MovieList.module.css";

interface MovieCardProps {
  movie?: Movie,
  disableLink?: boolean,
  onClick?: () => void,
}

const MovieCard: React.FC<MovieCardProps> = ({ movie, disableLink = false, onClick }) => {

  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>) => {
    e.currentTarget.src =
      "https://thumbs.dreamstime.com/b/film-real-25021714.jpg";
  };

  if (!movie) {
    return (<div className={`${styles.movie} skeleton`}>
      <div className={styles.skeletonPoster}></div>
    </div>)
  }

  const content = (
    <>
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
        <div className={styles.movieRating}>★ {movie.imdb.rating}</div>
      )}
    </>
  );

  if (disableLink) {
    return (
      <div className={styles.movie} onClick={onClick}>
        {content}
      </div>
    );
  }

  return (
    <div className={styles.movie}>
      <Link to={`/movie/${movie._id}`} className={styles.movieLink}>
        {content}
      </Link>
    </div>
  );
}

export default MovieCard
