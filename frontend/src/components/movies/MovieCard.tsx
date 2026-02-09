import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Image, Badge } from "../ui";
import { AnimationVariants } from "../../utils/animationVariants";
import { Movie } from "../../types";
import styles from "../../styles/components/movies/MovieList.module.css";

interface MovieCardProps {
  movie?: Movie,
  disableLink?: boolean,
  onClick?: () => void,
}

const MovieCard: React.FC<MovieCardProps> = ({ movie, disableLink = false, onClick }) => {

  if (!movie) {
    return (<div className={`${styles.movie} skeleton`}>
      <div className={styles.skeletonPoster}></div>
    </div>)
  }

  const content = (
    <>
      <Image
        src={movie.poster}
        alt={movie.title}
        className={styles.moviePoster}
        animation="zoom"
        size="auto"
        rounded="lg"
      />
      <motion.div 
        className={styles.movieHoverText}
        initial={{ opacity: 0, y: 20 }}
        whileHover={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.2, ease: [0.4, 0, 0.2, 1] }}
      >
        {movie.title}
      </motion.div>
      {movie.year && (
        <Badge
          variant="info"
          size="sm"
          position="top-left"
          className={styles.movieYear}
          animation="scale"
        >
          {movie.year}
        </Badge>
      )}
      {movie.imdb?.rating && (
        <Badge
          variant="success"
          size="sm"
          position="top-right"
          className={styles.movieRating}
          animation="scale"
        >
          ★ {movie.imdb.rating}
        </Badge>
      )}
    </>
  );

  if (disableLink) {
    return (
      <motion.div 
        className={styles.movie} 
        onClick={onClick}
        whileHover={AnimationVariants.movieCard.whileHover}
        whileTap={AnimationVariants.movieCard.whileTap}
        transition={AnimationVariants.movieCard.transition as any}
      >
        {content}
      </motion.div>
    );
  }

  return (
    <motion.div 
      className={styles.movie}
      whileHover={AnimationVariants.movieCard.whileHover}
      whileTap={AnimationVariants.movieCard.whileTap}
      transition={AnimationVariants.movieCard.transition as any}
    >
      <Link to={`/movie/${movie._id}`} className={styles.movieLink}>
        {content}
      </Link>
    </motion.div>
  );
}

export default MovieCard
