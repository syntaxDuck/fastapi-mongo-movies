/**
 * Filter Builder Utility for constructing dynamic movie query parameters
 * Transforms frontend filter objects into backend-compatible API parameters
 */

export interface MovieFilters {
  // Basic filters
  id?: string;
  title?: string;
  type?: string;
  search?: string;
  
  // Array filters
  genres?: string[];
  cast?: string[];
  directors?: string[];
  writers?: string[];
  countries?: string[];
  
  // Numeric filters
  year?: number;
  minYear?: number;
  maxYear?: number;
  runtime?: number;
  minRuntime?: number;
  maxRuntime?: number;
  num_mflix_comments?: number;
  minComments?: number;
  maxComments?: number;
  
  // Rating filters
  minRating?: number;
  maxRating?: number;
  ratingSource?: 'imdb' | 'tomatoes';
  
  // Date filters
  released?: Date;
  releasedAfter?: Date;
  releasedBefore?: Date;
  lastupdated?: Date;
  
  // Awards filter
  awards?: Record<string, any>;
  
  // Display options
  include_invalid_posters?: boolean;
  limit?: number;
  skip?: number;
  
  // Sort options
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface QueryParams extends Record<string, any> {
  id?: string;
  title?: string;
  type?: string;
  search?: string;
  genres?: string[];
  cast?: string[];
  directors?: string[];
  writers?: string[];
  countries?: string[];
  year?: number;
  runtime?: number;
  num_mflix_comments?: number;
  released?: string;
  lastupdated?: string;
  awards?: Record<string, any>;
  include_invalid_posters?: boolean;
  limit?: number;
  skip?: number;
}

/**
 * Filter Builder class for constructing movie query parameters
 */
export class FilterBuilder {
  /**
   * Convert frontend filter object to backend API parameters
   */
  static buildQueryParams(filters: MovieFilters): QueryParams {
    const params: QueryParams = {};

    // Basic string filters
    if (filters.id) params.id = filters.id;
    if (filters.title) params.title = filters.title;
    if (filters.type) params.type = filters.type;
    if (filters.search) params.search = filters.search;

    // Array filters
    if (filters.genres && filters.genres.length > 0) params.genres = filters.genres;
    if (filters.cast && filters.cast.length > 0) params.cast = filters.cast;
    if (filters.directors && filters.directors.length > 0) params.directors = filters.directors;
    if (filters.writers && filters.writers.length > 0) params.writers = filters.writers;
    if (filters.countries && filters.countries.length > 0) params.countries = filters.countries;

    // Numeric filters - handle single values and ranges
    if (filters.year !== undefined) {
      params.year = filters.year;
    } else if (filters.minYear !== undefined || filters.maxYear !== undefined) {
      // For range filtering, we'll use the single year field
      // The backend will need to handle range logic or we'll need separate endpoints
      if (filters.minYear !== undefined) params.year = filters.minYear;
      if (filters.maxYear !== undefined) params.year = filters.maxYear;
    }

    if (filters.runtime !== undefined) {
      params.runtime = filters.runtime;
    } else if (filters.minRuntime !== undefined || filters.maxRuntime !== undefined) {
      if (filters.minRuntime !== undefined) params.runtime = filters.minRuntime;
      if (filters.maxRuntime !== undefined) params.runtime = filters.maxRuntime;
    }

    if (filters.num_mflix_comments !== undefined) {
      params.num_mflix_comments = filters.num_mflix_comments;
    } else if (filters.minComments !== undefined || filters.maxComments !== undefined) {
      if (filters.minComments !== undefined) params.num_mflix_comments = filters.minComments;
      if (filters.maxComments !== undefined) params.num_mflix_comments = filters.maxComments;
    }

    // Date filters - convert to ISO strings
    if (filters.released) {
      params.released = filters.released.toISOString();
    }
    if (filters.releasedAfter) {
      params.released = filters.releasedAfter.toISOString();
    }
    if (filters.releasedBefore) {
      params.released = filters.releasedBefore.toISOString();
    }
    if (filters.lastupdated) {
      params.lastupdated = filters.lastupdated.toISOString();
    }

    // Awards filter
    if (filters.awards) {
      params.awards = filters.awards;
    }

    // Display options
    if (filters.include_invalid_posters !== undefined) {
      params.include_invalid_posters = filters.include_invalid_posters;
    }
    if (filters.limit !== undefined) {
      params.limit = filters.limit;
    }
    if (filters.skip !== undefined) {
      params.skip = filters.skip;
    }

    // Sort options
    if (filters.sort_by) {
      params.sort_by = filters.sort_by;
    }
    if (filters.sort_order) {
      params.sort_order = filters.sort_order;
    }

    return params;
  }

  /**
   * Check if any filters are active
   */
  static hasActiveFilters(filters: MovieFilters): boolean {
    return Object.values(filters).some(value => {
      if (value === undefined || value === null) return false;
      if (Array.isArray(value)) return value.length > 0;
      if (typeof value === 'object') return Object.keys(value).length > 0;
      return true;
    });
  }

  /**
   * Get a summary of active filters for display purposes
   */
  static getFilterSummary(filters: MovieFilters): string[] {
    const summary: string[] = [];

    if (filters.search) summary.push(`Search: "${filters.search}"`);
    if (filters.genres?.length) summary.push(`Genres: ${filters.genres.join(', ')}`);
    if (filters.directors?.length) summary.push(`Directors: ${filters.directors.join(', ')}`);
    if (filters.cast?.length) summary.push(`Cast: ${filters.cast.join(', ')}`);
    if (filters.year) summary.push(`Year: ${filters.year}`);
    if (filters.minYear && filters.maxYear) summary.push(`Years: ${filters.minYear}-${filters.maxYear}`);
    else if (filters.minYear) summary.push(`From: ${filters.minYear}`);
    else if (filters.maxYear) summary.push(`To: ${filters.maxYear}`);
    if (filters.type) summary.push(`Type: ${filters.type}`);
    if (filters.minRating) summary.push(`Min Rating: ${filters.minRating}`);
    if (filters.maxRating) summary.push(`Max Rating: ${filters.maxRating}`);
    if (filters.runtime) summary.push(`Runtime: ${filters.runtime}min`);
    if (filters.include_invalid_posters) summary.push('Include invalid posters');

    return summary;
  }

  /**
   * Create a copy of filters with pagination removed
   */
  static removePagination(filters: MovieFilters): MovieFilters {
    const { limit, skip, ...rest } = filters;
    return rest;
  }

  /**
   * Validate filter values
   */
  static validateFilters(filters: MovieFilters): { isValid: boolean; errors: string[] } {
    const errors: string[] = [];

    // Validate numeric ranges
    if (filters.minYear !== undefined && filters.maxYear !== undefined) {
      if (filters.minYear > filters.maxYear) {
        errors.push('minYear cannot be greater than maxYear');
      }
    }

    if (filters.minRating !== undefined && filters.maxRating !== undefined) {
      if (filters.minRating > filters.maxRating) {
        errors.push('minRating cannot be greater than maxRating');
      }
    }

    if (filters.minRuntime !== undefined && filters.maxRuntime !== undefined) {
      if (filters.minRuntime > filters.maxRuntime) {
        errors.push('minRuntime cannot be greater than maxRuntime');
      }
    }

    // Validate year ranges
    const currentYear = new Date().getFullYear();
    if (filters.year && (filters.year < 1800 || filters.year > currentYear + 10)) {
      errors.push(`Year must be between 1800 and ${currentYear + 10}`);
    }
    if (filters.minYear && (filters.minYear < 1800 || filters.minYear > currentYear + 10)) {
      errors.push(`minYear must be between 1800 and ${currentYear + 10}`);
    }
    if (filters.maxYear && (filters.maxYear < 1800 || filters.maxYear > currentYear + 10)) {
      errors.push(`maxYear must be between 1800 and ${currentYear + 10}`);
    }

    // Validate rating ranges
    if (filters.minRating !== undefined && (filters.minRating < 0 || filters.minRating > 10)) {
      errors.push('minRating must be between 0 and 10');
    }
    if (filters.maxRating !== undefined && (filters.maxRating < 0 || filters.maxRating > 10)) {
      errors.push('maxRating must be between 0 and 10');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }
}

/**
 * Default filter values
 */
export const DEFAULT_FILTERS: Partial<MovieFilters> = {
  include_invalid_posters: false,
  limit: 24,
  skip: 0
};

/**
 * Helper function to create a new filter object with defaults
 */
export function createFilters(overrides: Partial<MovieFilters> = {}): MovieFilters {
  return {
    ...DEFAULT_FILTERS,
    ...overrides
  } as MovieFilters;
}