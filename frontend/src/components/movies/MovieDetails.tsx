import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { Movie } from "../../types";
import { movieService } from "../../services/api";
import {
  ImdbRating,
  TomatoesCriticRating,
  TomatoesViewerRating,
} from "./MovieRating";
import styles from "../../styles/components/movies/MovieDetails.module.css";

const MovieDetail: React.FC<{ name: string; key: string; item: any }> = ({
  name,
  key: itemKey,
  item,
}) => {
  if (!item || item[itemKey] === undefined || item[itemKey] === null) {
    return (
      <p>
        <strong>{name}:</strong> N/A
      </p>
    );
  }

  const value = item[itemKey];
  const displayValue = Array.isArray(value) ? value.join(", ") : value;

  return (
    <p>
      <strong>{name}:</strong> {displayValue}
    </p>
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
        <MovieDetail name="Genres" key="genres" item={movie} />
        <hr />
        <MovieDetail name="Directors" key="directors" item={movie} />
        <hr />
        <MovieDetail name="Writers" key="writers" item={movie} />
        <hr />
        <MovieDetail name="Cast" key="cast" item={movie} />
        <hr />
        <MovieDetail name="Countries" key="countries" item={movie} />
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
    return <div className={styles.loading}>Loading movie details...</div>;
  }

  if (error) {
    return <div className={styles.error}>Failed to load movie details</div>;
  }

  if (!movie) {
    return <div className={styles.error}>Movie not found</div>;
  }

  return (
    <div className={styles.movieDetails}>
      <MovieDetailsHeader movie={movie} />
      <MovieDetailsBody movie={movie} />
      <MoviePlot movie={movie} />
    </div>
  );
};

export default MovieDetails;
