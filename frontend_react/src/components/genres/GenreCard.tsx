import React from "react";
import { Link } from "react-router-dom";
import { Movie } from "../../types";
import styles from "../../styles/components/genres/GenreCard.module.css";

interface GenreCardProps {
  genre?: string,
  movie?: Movie,
}

const GenreCard: React.FC<GenreCardProps> = ({ genre, movie }) => {

  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>) => {
    e.currentTarget.src =
      "https://thumbs.dreamstime.com/b/film-real-25021714.jpg";
  };

  if (!movie) {
    return (<div className={`${styles.genreCard} ${styles.skeleton}`}>
      <div className={styles.skeletonTitle}></div>
      <div className={styles.skeletonPoster}></div>
    </div>)
  }

  return (
    <div className={styles.genreCard}>
      <h3 className={styles.genreTitle}>{genre}</h3>
      <Link to={`/genres/${genre}`} className={styles.genreLink}>
        <img
          src={movie.poster}
          alt={movie.title}
          onError={handleImageError}
          className={styles.genrePoster}
          loading="lazy"
        />
        <div className={styles.genreOverlay}>
          Explore {genre} movies
        </div>
        <div className={styles.genreBadge}>
          Browse
        </div>
      </Link>
    </div>
  )
}

export default GenreCard
