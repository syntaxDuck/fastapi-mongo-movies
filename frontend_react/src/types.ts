export interface Movie {
  _id: string;
  title: string;
  plot: string;
  fullplot?: string;
  genres: string[];
  cast: string[];
  directors: string[];
  writers?: string[];
  countries?: string[];
  year: number;
  runtime: number;
  type: string;
  poster: string;
  imdb?: {
    rating: number;
    votes: number;
    id: number;
  };
  tomatoes?: {
    critic?: {
      rating: number;
      numReviews: number;
    };
    viewer?: {
      rating: number;
      numReviews: number;
    };
  } | null;
}

export interface Comment {
  _id: string;
  movie_id: string;
  name: string;
  email: string;
  text: string;
  date: string;
}

export interface ApiResponse<T> {
  data: T[];
  total?: number;
  page?: number;
  limit?: number;
}
