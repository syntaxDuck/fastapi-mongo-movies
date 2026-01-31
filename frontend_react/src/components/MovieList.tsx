import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { Movie } from '../types';
import { movieService } from '../services/api';
import './MovieList.css';

interface MovieListProps {
  filter?: {
    genre?: string;
    director?: string;
    minYear?: number;
    maxYear?: number;
    minRating?: number;
  };
}

const MovieList: React.FC<MovieListProps> = ({ filter }) => {
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const pageSize = 20;

  const loadMovies = useCallback(async (pageNum: number, reset = false) => {
    try {
      setLoading(true);
      const params = {
        type: 'movie',
        skip: pageNum * pageSize,
        limit: pageSize,
        ...filter
      };
      
      const newMovies = await movieService.fetchMovies(params);
      
      if (reset) {
        setMovies(newMovies);
      } else {
        setMovies(prev => [...prev, ...newMovies]);
      }
      
      setHasMore(newMovies.length === pageSize);
      setError(null);
    } catch (err) {
      setError('Failed to load movies');
      console.error('Error loading movies:', err);
    } finally {
      setLoading(false);
    }
  }, [filter, pageSize]);

  useEffect(() => {
    setPage(0);
    loadMovies(0, true);
  }, [filter, loadMovies]);

  const loadMore = () => {
    const nextPage = page + 1;
    setPage(nextPage);
    loadMovies(nextPage, false);
  };

  const handleImageError = (e: React.SyntheticEvent<HTMLImageElement>) => {
    e.currentTarget.src = 'https://thumbs.dreamstime.com/b/film-real-25021714.jpg';
  };

  if (loading && movies.length === 0) {
    return <div className="loading">Loading movies...</div>;
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  return (
    <div className="movie-list-container">
      <ul className="movie-list">
        {movies.map((movie, index) => (
          <li key={`${movie._id}-${index}`} className="movie">
            <Link to={`/movie/${movie._id}`}>
              <img
                src={movie.poster}
                alt={movie.title}
                onError={handleImageError}
                className="movie-poster"
              />
              <span className="movie-hover-text">{movie.title}</span>
            </Link>
          </li>
        ))}
      </ul>
      
      {hasMore && (
        <div className="load-more-container">
          <button 
            onClick={loadMore} 
            disabled={loading}
            className="load-more-btn"
          >
            {loading ? 'Loading...' : 'Next ▷'}
          </button>
        </div>
      )}
      
      {!hasMore && movies.length > 0 && (
        <p className="no-more">No more movies to load</p>
      )}
    </div>
  );
};

export default MovieList;