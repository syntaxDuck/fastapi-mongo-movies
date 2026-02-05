import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
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
      <motion.img
        src={movie.poster}
        alt={movie.title}
        onError={handleImageError}
        className={styles.moviePoster}
        loading="lazy"
        whileHover={{ scale: 1.08, filter: "brightness(1.05)" }}
        transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }}
        style={{ filter: "brightness(0.95)" }}
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
        <motion.div 
          className={styles.movieYear}
          whileHover={{ scale: 1.05 }}
          transition={{ duration: 0.2 }}
        >
          {movie.year}
        </motion.div>
      )}
      {movie.imdb?.rating && (
        <motion.div 
          className={styles.movieRating}
          whileHover={{ scale: 1.05 }}
          transition={{ duration: 0.2 }}
        >
          ★ {movie.imdb.rating}
        </motion.div>
      )}
    </>
  );

  if (disableLink) {
    return (
      <motion.div 
        className={styles.movie} 
        onClick={onClick}
        whileHover={{ y: -6, scale: 1.02 }}
        whileTap={{ scale: 0.98, y: -3 }}
        transition={{ duration: 0.2, ease: [0.4, 0, 0.2, 1] }}
      >
        {content}
      </motion.div>
    );
  }

  return (
    <motion.div 
      className={styles.movie}
      whileHover={{ y: -6, scale: 1.02 }}
      whileTap={{ scale: 0.98, y: -3 }}
      transition={{ duration: 0.2, ease: [0.4, 0, 0.2, 1] }}
    >
      <Link to={`/movie/${movie._id}`} className={styles.movieLink}>
        {content}
      </Link>
    </motion.div>
  );
}

export default MovieCard
