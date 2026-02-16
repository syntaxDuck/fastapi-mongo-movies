import React, { memo, useCallback } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Image, Badge } from "../ui";
import { AnimationVariants } from "../../utils/animationVariants";
import { Movie } from "../../types";
import styles from "../../styles/components/movies/MovieList.module.css";

const MotionLink = motion(Link);

interface MovieCardProps {
  movie?: Movie;
  disableLink?: boolean;
  onMovieClick?: (movieId: string) => void;
}

const overlayVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

const cardVariants = {
  hidden: { y: 0, scale: 1 },
  visible: AnimationVariants.movieCard.whileHover,
  tap: AnimationVariants.movieCard.whileTap
};

/**
 * Optimized MovieCard component with memoization to prevent unnecessary re-renders.
 * Enhanced with focus states and keyboard accessibility for better UX.
 */
const MovieCard: React.FC<MovieCardProps> = memo(({ movie, disableLink = false, onMovieClick }) => {

  const handleInternalClick = useCallback(() => {
    if (onMovieClick && movie?._id) {
      onMovieClick(movie._id);
    }
  }, [onMovieClick, movie?._id]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleInternalClick();
    }
  }, [handleInternalClick]);

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
        variants={overlayVariants}
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
        onClick={handleInternalClick}
        onKeyDown={handleKeyDown}
        tabIndex={0}
        role="button"
        aria-label={`View details for ${movie.title}`}
        initial="hidden"
        whileHover="visible"
        whileFocus="visible"
        whileTap="tap"
        variants={cardVariants}
        transition={AnimationVariants.movieCard.transition}
      >
        {content}
      </motion.div>
    );
  }

  return (
    <motion.div 
      className={styles.movie}
      transition={AnimationVariants.movieCard.transition}
    >
      <MotionLink
        to={`/movie/${movie._id}`}
        className={styles.movieLink}
        aria-label={`View details for ${movie.title}`}
        initial="hidden"
        whileHover="visible"
        whileFocus="visible"
        whileTap="tap"
        variants={cardVariants}
      >
        {content}
      </MotionLink>
    </motion.div>
  );
});

MovieCard.displayName = "MovieCard";

export default MovieCard;
