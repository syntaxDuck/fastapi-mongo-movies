import { Movie, Comment } from "../types";

const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const movieService = {
  async fetchMovies(params?: {
    type?: string;
    skip?: number;
    limit?: number;
    genre?: string;
    director?: string;
    minYear?: number;
    maxYear?: number;
    minRating?: number;
    search?: string;
    include_invalid_posters?: boolean;
  }): Promise<Movie[]> {
    const queryParams = new URLSearchParams();

    // Always include include_invalid_posters=false unless explicitly set to true
    const finalParams = { include_invalid_posters: false, ...params };

    Object.entries(finalParams).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        queryParams.append(key, value.toString());
      }
    });

    const response = await fetch(
      `${API_BASE_URL}/movies/?${queryParams.toString()}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      },
    );

    if (!response.ok) {
      const errorText = await response.text();
      console.error("API Error:", response.status, errorText);
      throw new Error(
        `HTTP error! status: ${response.status}, message: ${errorText}`,
      );
    }

    const data = await response.json();
    return processMovies(data);
  },

  async getMovieById(movieId: string): Promise<Movie> {
    const response = await fetch(`${API_BASE_URL}/movies/${movieId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });
    if (!response.ok) {
      const errorText = await response.text();
      console.error("API Error:", response.status, errorText);
      throw new Error(
        `HTTP error! status: ${response.status}, message: ${errorText}`,
      );
    }

    const data = await response.json();
    return processMovies([data])[0];
  },

  async getMovieByGenre(genre: string, params?: {
    type?: string;
    skip?: number;
    limit?: number;
    include_invalid_posters?: boolean;
  }): Promise<Movie[]> {
    const queryParams = new URLSearchParams();

    // Always include include_invalid_posters=false unless explicitly set to true
    const finalParams = { include_invalid_posters: false, ...params };

    Object.entries(finalParams).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        queryParams.append(key, value.toString());
      }
    });

    const response = await fetch(`${API_BASE_URL}/movies/genres/${genre}/?${queryParams.toString()}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });
    if (!response.ok) {
      const errorText = await response.text();
      console.error("API Error:", response.status, errorText);
      throw new Error(
        `HTTP error! status: ${response.status}, message: ${errorText}`,
      );
    }

    const data = await response.json();
    return processMovies(data);
  },

  async getMovieGenres(): Promise<Array<string>> {
    const response = await fetch(`${API_BASE_URL}/movies/genres`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
    });
    if (!response.ok) {
      const errorText = await response.text();
      console.error("API Error:", response.status, errorText);
      throw new Error(
        `HTTP error! status: ${response.status}, message: ${errorText}`,
      );
    }

    return response.json();
  }
};

export const commentService = {
  async fetchComments(movie_id: string, params?: any): Promise<Comment[]> {

    const queryParams = new URLSearchParams();

    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          queryParams.append(key, value.toString());
        }
      });
    }
    const response = await fetch(
      `${API_BASE_URL}/comments/movie/${movie_id}/?${queryParams.toString()}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      },
    );
    if (!response.ok) {
      const errorText = await response.text();
      console.error("API Error:", response.status, errorText);
      throw new Error(
        `HTTP error! status: ${response.status}, message: ${errorText}`,
      );
    }

    return await response.json();
  },
};

function processMovies(movies: Movie[]): Movie[] {
  const defaultImg = "https://thumbs.dreamstime.com/b/film-real-25021714.jpg";

  return movies.map((movie) => {
    if (movie.poster && movie.valid_poster === true) {
      return movie;
    } else {
      return {
        ...movie,
        poster: defaultImg,
      };
    }
  });
}
