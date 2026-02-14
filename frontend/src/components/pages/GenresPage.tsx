import React, { useMemo } from "react";
import { motion } from "framer-motion";
import { Movie } from "../../types";
import { movieService } from "../../services/api";
import styles from "../../styles/components/pages/GenresPage.module.css";
import GenreCard from "../genres/GenreCard";
import { LoadingWrapper, LoadingSpinners } from "../ui/LoadingComponents";
import { useMovieGenres } from "../../hooks";

const GenresPage: React.FC = () => {
  const { data: genreTypes, isLoading, error, refetch } = useMovieGenres();

  const genreMovies = useMemo(() => {
    if (!genreTypes) return [];
    return genreTypes.map((genre) => ({ genre }));
  }, [genreTypes]);

  const handleRetry = () => {
    refetch();
  };

  const loadGenres = async () => {
    if (!genreTypes) return;
    
    const genreMoviesPromises = genreTypes.map(async (genre) => {
      try {
        const movie_batch = await movieService.getMovieByGenre(genre, {
          limit: 5,
        });
        return { genre, movie_batch };
      } catch (e) {
        console.warn(`Failed to load movies for genre ${genre}:`, e);
        return { genre, movie_batch: [] };
      }
    });

    const results = await Promise.all(genreMoviesPromises);

    const usedMovieIds = new Set<string>();
    const finalGenres: { genre: string; movie: Movie }[] = [];

    for (const { genre, movie_batch } of results) {
      const uniqueMovie = movie_batch.find((m) => !usedMovieIds.has(m._id));

      if (uniqueMovie) {
        usedMovieIds.add(uniqueMovie._id);
        finalGenres.push({ genre, movie: uniqueMovie });
      } else {
        console.debug(
          `Skipping genre ${genre} - no unique poster available in batch`,
        );
      }
    }

    return finalGenres;
  };

  if (isLoading) {
    return (
      <div className={styles.genresPageContainer}>
        <motion.div
          className={styles.genresHeader}
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className={styles.genresTitle}>Movie Genres</h1>
          <p className={styles.genresSubtitle}>
            Explore our collection by genre
          </p>
        </motion.div>

        <LoadingWrapper
          isLoading={true}
          children={null}
          fallback={
            <motion.div
              className={styles.genresGrid}
              initial="hidden"
              animate="visible"
            >
              {Array.from({ length: 12 }, (_, i) => (
                <motion.div
                  key={`skeleton-${i}`}
                  className={styles.genreCardSkeleton}
                  role="status"
                  aria-label={`Loading genre ${i + 1}`}
                >
                  <div className={styles.skeletonPoster}>
                    <LoadingSpinners.Default
                      size="sm"
                      color="gray"
                      type="dots"
                    />
                  </div>
                  <div className={styles.skeletonTitle}></div>
                </motion.div>
              ))}
            </motion.div>
          }
        />
      </div>
    );
  }

  if (error) {
    return (
      <div className={styles.genresPageContainer}>
        <motion.div
          className={styles.errorContainer}
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
        >
          <div className={styles.errorIcon}>⚠️</div>
          <h2>Oops! Something went wrong</h2>
          <p>Failed to load genres</p>
          <motion.button
            className={styles.retryButton}
            onClick={handleRetry}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            Try Again
          </motion.button>
        </motion.div>
      </div>
    );
  }

  return (
    <GenresContent genreTypes={genreTypes || []} loadGenres={loadGenres} />
  );
};

interface GenresContentProps {
  genreTypes: string[];
  loadGenres: () => Promise<{ genre: string; movie: Movie }[] | undefined>;
}

const GenresContent: React.FC<GenresContentProps> = ({ genreTypes, loadGenres }) => {
  const [genres, setGenres] = React.useState<{ genre: string; movie: Movie }[]>([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    const fetchGenreMovies = async () => {
      setLoading(true);
      const results = await loadGenres();
      if (results) {
        setGenres(results);
      }
      setLoading(false);
    };
    fetchGenreMovies();
  }, [genreTypes, loadGenres]);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const cardVariants = {
    hidden: { opacity: 0, y: 30 },
    visible: { opacity: 1, y: 0 },
  };

  if (loading) {
    return (
      <div className={styles.genresPageContainer}>
        <motion.div
          className={styles.genresHeader}
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h1 className={styles.genresTitle}>Movie Genres</h1>
          <p className={styles.genresSubtitle}>
            Explore our collection by genre
          </p>
        </motion.div>

        <LoadingWrapper
          isLoading={true}
          children={null}
          fallback={
            <motion.div
              className={styles.genresGrid}
              initial="hidden"
              animate="visible"
            >
              {Array.from({ length: 12 }, (_, i) => (
                <motion.div
                  key={`skeleton-${i}`}
                  className={styles.genreCardSkeleton}
                  role="status"
                  aria-label={`Loading genre ${i + 1}`}
                >
                  <div className={styles.skeletonPoster}>
                    <LoadingSpinners.Default
                      size="sm"
                      color="gray"
                      type="dots"
                    />
                  </div>
                  <div className={styles.skeletonTitle}></div>
                </motion.div>
              ))}
            </motion.div>
          }
        />
      </div>
    );
  }

  return (
    <div className={styles.genresPageContainer}>
      <motion.div
        className={styles.genresHeader}
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1 className={styles.genresTitle}>Movie Genres</h1>
        <p className={styles.genresSubtitle}>
          Discover {genres.length} different genres from our collection
        </p>
      </motion.div>

      <motion.div
        className={styles.genresGrid}
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {genres.map((genre, index) => (
          <motion.div
            key={`${genre.genre}-${index}`}
            variants={cardVariants}
            whileHover={{ y: -8, scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            transition={{ duration: 0.2 }}
          >
            <GenreCard genre={genre.genre} movie={genre.movie} />
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
};

export default GenresPage;
