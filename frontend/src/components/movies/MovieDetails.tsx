import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { Movie } from "../../types";
import { movieService } from "../../services/api";
import {
  ImdbRating,
  TomatoesCriticRating,
  TomatoesViewerRating,
} from "./MovieRating";
import styles from "../../styles/components/movies/MovieDetails.module.css";
import { CenteredLoading } from "../ui/LoadingComponents";

const MovieDetail: React.FC<{ name: string; value: string; item: any }> = ({
  name,
  value,
  item,
}) => {
  if (!item || item[value] === undefined || item[value] === null) {
    return (
      <p>
        <strong>{name}:</strong> N/A
      </p>
    );
  }

  const displayValue = Array.isArray(item[value]) ? item[value].join(", ") : item[value];

  return (
    <p style={{
      display: "grid", gridTemplateColumns: "12ch 1fr", gap: "10px", alignItems: "start"
    }}>
      <strong>{name}:</strong> <span>{displayValue}</span>
    </p >
  );
};

const MovieDetailsHeader: React.FC<{ movie: Movie }> = ({ movie }) => {
  const data = `${movie.year}・${Math.floor(movie.runtime / 60)}h ${movie.runtime % 60}m`;

  return (
    <div className={styles.movieDetailsHeader}>
      <h1>{movie.title}</h1>
      <div className={styles.movieDetailsMeta}>
        <p>{data}</p>
      </div>
    </div>
  );
};

const MovieDetailsBody: React.FC<{ movie: Movie }> = ({ movie }) => {
  const tomatoesCritic = TomatoesCriticRating({ tomatoes: movie.tomatoes });
  const tomatoesViewer = TomatoesViewerRating({ tomatoes: movie.tomatoes });
  const imdb = ImdbRating({ movie });

  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>) => {
    e.currentTarget.src =
      "https://thumbs.dreamstime.com/b/film-real-25021714.jpg";
  };

  return (
    <div className={styles.movieDetailsBody}>
      <img
        src={movie.poster}
        alt={movie.title}
        onError={handleImageError}
        className={styles.movieDetailsPoster}
      />
      <div className={styles.movieDetailsInfo}>
        <MovieDetail name="Genres" value="genres" item={movie} />
        <hr />
        <MovieDetail name="Directors" value="directors" item={movie} />
        <hr />
        <MovieDetail name="Writers" value="writers" item={movie} />
        <hr />
        <MovieDetail name="Cast" value="cast" item={movie} />
        <hr />
        <MovieDetail name="Countries" value="countries" item={movie} />
        <hr />
        <div className={styles.movieDetailsRatings}>
          {imdb}
          {tomatoesCritic}
          {tomatoesViewer}
        </div>
      </div>
    </div>
  );
};

const MoviePlot: React.FC<{ movie: Movie }> = ({ movie }) => {
  const plotText =
    movie.fullplot && movie.fullplot.trim().length > 0
      ? movie.fullplot
      : movie.plot;

  return (
    <div className={styles.movieDetailsPlot}>
      <p>{plotText}</p>
    </div>
  );
};

interface MovieDetailsProps {
  id?: string;
  movie?: Movie; // Allow passing movie data directly
}

const MovieDetails: React.FC<MovieDetailsProps> = ({ id = "", movie: propMovie }) => {
  const { movieId } = useParams<{ movieId: string }>();
  const [movie, setMovie] = useState<Movie | null>(propMovie || null);
  const [loading, setLoading] = useState(!propMovie); // Don't load if movie is passed as prop
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // If movie is passed as prop, use it directly
    if (propMovie) {
      setMovie(propMovie);
      setLoading(false);
      return;
    }

    // Otherwise load movie by ID
    const loadMovie = async () => {
      const targetId = id || movieId;
      if (!targetId) return;

      try {
        setLoading(true);
        const movieData = await movieService.getMovieById(targetId);
        setMovie(movieData);
        setError(null);
      } catch (err) {
        setError("Failed to load movie details");
        console.error("Error loading movie:", err);
      } finally {
        setLoading(false);
      }
    };

    loadMovie();
  }, [movieId, id, propMovie]);

  if (loading) {
    return (
      <CenteredLoading
        message="Loading movie details..."
        spinnerProps={{ size: "lg", color: "accent", type: "ring" }}
        className={styles.loading}
      />
    );
  }

  if (error) {
    return <div className={styles.error}>Failed to load movie details</div>;
  }

  if (!movie) {
    return <div className={styles.error}>Movie not found</div>;
  }

  return (
    <motion.div
      className={styles.movieDetails}
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, ease: [0.4, 0, 0.2, 1] }}
    >
      <MovieDetailsHeader movie={movie} />
      <MovieDetailsBody movie={movie} />
      <MoviePlot movie={movie} />
    </motion.div>
  );
};

export default MovieDetails;
