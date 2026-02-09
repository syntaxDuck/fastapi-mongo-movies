import React from "react";
import { Link } from "react-router-dom";
import { Image, Badge } from "../ui";
import { Movie } from "../../types";
import styles from "../../styles/components/genres/GenreCard.module.css";

interface GenreCardProps {
  genre?: string,
  movie?: Movie,
}

const GenreCard: React.FC<GenreCardProps> = ({ genre, movie }) => {

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
        <Image
          src={movie.poster}
          alt={movie.title}
          className={styles.genrePoster}
          animation="zoom"
          size="auto"
          rounded="lg"
        />
        <div className={styles.genreOverlay}>
          Explore {genre} movies
        </div>
        <Badge
          variant="default"
          size="sm"
          position="top-right"
          className={styles.genreBadge}
          animation="scale"
        >
          Browse
        </Badge>
      </Link>
    </div>
  )
}

export default GenreCard
