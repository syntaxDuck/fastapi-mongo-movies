import React, { useState, useEffect } from "react";
import { motion, scale, Variants } from "framer-motion";
import MovieDetails from "../movies/MovieDetails";
import MovieList from "../movies/MovieList";
import { MovieFilters } from "../../utils/filterBuilder";
import styles from "../../styles/components/pages/MoviePage.module.css";
import { AnimationVariants } from "../ui";

function useMediaQuery(query: string) {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    if (media.matches !== matches) {
      setMatches(media.matches);
    }

    const listener = () => setMatches(media.matches);
    media.addEventListener('change', listener);

    return () => media.removeEventListener('change', listener);
  }, [matches, query]);

  return matches;
}

interface MoviePageProps {
  filter?: MovieFilters;
}

const MoviePage: React.FC<MoviePageProps> = ({ filter }) => {
  const [selectedMovie, setSelectedMovie] = useState("");

  const handleMovieSelect = (movieId: string) => {
    setSelectedMovie(movieId)
  }

  const isDesktop = useMediaQuery('(min-width: 1025px)');

  const movieListVariants: Variants = {
    hidden: {
      x: -400,
      opacity: 0
    },
    visible: {
      x: 0,
      opacity: 1,
      transition: {
        ease: "easeIn",
        type: "spring",
        stiffness: 350,
        damping: 28
      }
    },
  }

  const badgesVariants: Variants = {
    hidden: {
      transition: {
        staggerChildren: 0.2
      }
    },
    visible: {
      transition: {
        staggerChildren: 0.2,
        delayChildren: 0.2
      }
    }
  }

  const badgeVariants: Variants = {
    hidden: {
      x: 300,
      opacity: 0
    },
    visible: {
      x: 0,
      opacity: 1,
      transition: {
        ease: "easeIn",
        type: "spring",
        stiffness: 350,
        damping: 28
      }
    },
  };

  //BUG: Movie Page Container error screen currently isn't styled properly
  return (
    <div className={styles.moviePageContainer}>
      {isDesktop && (
        <>
          <motion.div variants={movieListVariants} initial="hidden" animate="visible">
            <MovieList filter={filter} onMovieSelect={handleMovieSelect} disableCardLink={isDesktop} />
          </motion.div>
          <div className={styles.movieDetailsContainer}>
            {selectedMovie ? (
              <MovieDetails id={selectedMovie} />
            ) : (
              <motion.div
                className={styles.selectMoviePrompt}
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, ease: [0.4, 0, 0.2, 1] }}
              >
                <motion.div className={styles.promptIcon}
                  animate={{
                    y: [0, -10, 2, 0],
                    rotate: [0, -10, 10, 0]
                  }}
                  transition={{
                    duration: 3,
                    ease: "easeInOut",
                  }}>
                  🎬
                </motion.div>
                <h2 className={styles.promptTitle}>Select a Movie</h2>
                <p className={styles.promptText}>
                  Choose a movie from the list to view its details, ratings, and additional information.
                </p>
                <motion.div className={styles.promptFeatures} variants={badgesVariants} initial="hidden" animate="visible">
                  <motion.div variants={badgeVariants}>
                    <motion.div className={styles.feature} whileHover={{ scale: 1.05 }}>
                      <span className={styles.featureIcon}>⭐</span>
                      <span className={styles.featureText}>Page Ratings</span>
                    </motion.div>
                  </motion.div>
                  <motion.div variants={badgeVariants}>
                    <motion.div className={styles.feature} whileHover={{ scale: 1.05 }}>
                      <span className={styles.featureIcon}>📽️</span>
                      <span className={styles.featureText}>Movie Details</span>
                    </motion.div>
                  </motion.div>
                  <motion.div variants={badgeVariants}>
                    <motion.div className={styles.feature} whileHover={{ scale: 1.05 }}>
                      <span className={styles.featureIcon}>🎭</span>
                      <span className={styles.featureText}>Cast & Crew</span>
                    </motion.div>
                  </motion.div>
                </motion.div>
              </motion.div>
            )}
          </div>
        </>)}
      {!isDesktop && (
        <MovieList filter={filter} onMovieSelect={handleMovieSelect} disableCardLink={isDesktop} />
      )}
    </div>
  );
}

export default MoviePage
