import { useQuery, useInfiniteQuery, useQueryClient } from "@tanstack/react-query";
import { Movie, Comment } from "../types";
import { movieService, commentService } from "../services/api";

const STALE_TIME = {
  MOVIES: 5 * 60 * 1000,
  MOVIE_BY_ID: 10 * 60 * 1000,
  GENRES: 24 * 60 * 60 * 1000,
  TYPES: 24 * 60 * 60 * 1000,
  COMMENTS: 2 * 60 * 1000,
};

const PAGE_SIZE = 24;

interface UseMoviesParams {
  type?: string;
  search?: string;
  genre?: string;
  year?: number;
  minYear?: number;
  maxYear?: number;
  minRating?: number;
  maxRating?: number;
  include_invalid_posters?: boolean;
}

export function useMovies(params?: UseMoviesParams) {
  return useInfiniteQuery<Movie[], Error>({
    queryKey: ["movies", params],
    queryFn: ({ pageParam = 0 }) => {
      const queryParams = {
        ...params,
        skip: (pageParam as number) * PAGE_SIZE,
        limit: PAGE_SIZE,
      };
      return movieService.fetchMovies(queryParams);
    },
    initialPageParam: 0,
    getNextPageParam: (lastPage, allPages) => {
      return lastPage.length === PAGE_SIZE ? allPages.length : undefined;
    },
    staleTime: STALE_TIME.MOVIES,
  });
}

export function useMovieById(movieId: string) {
  return useQuery<Movie, Error>({
    queryKey: ["movie", movieId],
    queryFn: () => movieService.getMovieById(movieId),
    enabled: !!movieId,
    staleTime: STALE_TIME.MOVIE_BY_ID,
  });
}

export function useMovieGenres() {
  return useQuery<string[], Error>({
    queryKey: ["movie-genres"],
    queryFn: () => movieService.getMovieGenres(),
    staleTime: STALE_TIME.GENRES,
  });
}

export function useMovieTypes() {
  return useQuery<string[], Error>({
    queryKey: ["movie-types"],
    queryFn: () => movieService.getMovieTypes(),
    staleTime: STALE_TIME.TYPES,
  });
}

export function useMovieByGenre(genre: string, params?: {
  type?: string;
  skip?: number;
  limit?: number;
  include_invalid_posters?: boolean;
}) {
  return useQuery<Movie[], Error>({
    queryKey: ["movies", "genre", genre, params],
    queryFn: () => movieService.getMovieByGenre(genre, params),
    enabled: !!genre,
    staleTime: STALE_TIME.MOVIES,
  });
}

export function useMovieComments(movieId: string) {
  return useQuery<Comment[], Error>({
    queryKey: ["comments", movieId],
    queryFn: () => commentService.fetchComments(movieId),
    enabled: !!movieId,
    staleTime: STALE_TIME.COMMENTS,
  });
}
