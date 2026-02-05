import React, { useState, useEffect } from "react";
import MovieDetails from "../movies/MovieDetails";
import MovieList from "../movies/MovieList";
import styles from "../../styles/components/movies/MovieView.module.css";

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

const MovieView: React.FC = () => {
  const [selectedMovie, setSelectedMovie] = useState("");

  const handleMovieSelect = (movieId: string) => {
    setSelectedMovie(movieId)
  }

  const isDesktop = useMediaQuery('(min-width: 1025px)');

  return (<div className={styles.movieViewContainer}>
    <MovieList onMovieSelect={handleMovieSelect} />
    {isDesktop && (<MovieDetails id={selectedMovie} />)}
  </div>)
}

export default MovieView
