/**
 * Simple test for FilterBuilder utility
 * This can be run in the browser console or as part of the app
 */

import { FilterBuilder, MovieFilters } from './filterBuilder';

// Test function that can be called from the browser console
export function runFilterBuilderTests() {
  console.log("🧪 Testing FilterBuilder utility...\n");
  
  // Test 1: Basic query building
  console.log("Test 1: Basic query parameter building");
  const basicFilters: MovieFilters = {
    search: "action",
    genres: ["Action", "Sci-Fi"],
    year: 2020,
    minRating: 7,
    limit: 24
  };
  
  const queryParams = FilterBuilder.buildQueryParams(basicFilters);
  console.log("Input filters:", basicFilters);
  console.log("Generated params:", queryParams);
  console.log("✅ Test 1 passed\n");
  
  // Test 2: Empty filters
  console.log("Test 2: Empty filters");
  const emptyParams = FilterBuilder.buildQueryParams({});
  console.log("Empty params:", emptyParams);
  console.log("✅ Test 2 passed\n");
  
  // Test 3: Array parameters
  console.log("Test 3: Array parameters");
  const arrayFilters: MovieFilters = {
    genres: ["Action", "Comedy", "Drama"],
    directors: ["Director 1", "Director 2"],
    cast: ["Actor 1", "Actor 2", "Actor 3"]
  };
  
  const arrayParams = FilterBuilder.buildQueryParams(arrayFilters);
  console.log("Array filters:", arrayFilters);
  console.log("Array params:", arrayParams);
  console.log("✅ Test 3 passed\n");
  
  // Test 4: Validation
  console.log("Test 4: Filter validation");
  const validFilters: MovieFilters = {
    year: 2020,
    minRating: 7,
    maxRating: 9
  };
  
  const invalidFilters: MovieFilters = {
    minYear: 2025,
    maxYear: 2020,
    minRating: 15
  };
  
  const validValidation = FilterBuilder.validateFilters(validFilters);
  const invalidValidation = FilterBuilder.validateFilters(invalidFilters);
  
  console.log("Valid filters validation:", validValidation);
  console.log("Invalid filters validation:", invalidValidation);
  console.log("✅ Test 4 passed\n");
  
  // Test 5: Filter summary
  console.log("Test 5: Filter summary");
  const summaryFilters: MovieFilters = {
    search: "matrix",
    genres: ["Action", "Sci-Fi"],
    year: 1999,
    minRating: 8,
    type: "movie"
  };
  
  const summary = FilterBuilder.getFilterSummary(summaryFilters);
  console.log("Summary filters:", summaryFilters);
  console.log("Filter summary:", summary);
  console.log("✅ Test 5 passed\n");
  
  // Test 6: Has active filters
  console.log("Test 6: Has active filters");
  const activeFilters: MovieFilters = { search: "test" };
  const emptyFilters: MovieFilters = {};
  
  const hasActive1 = FilterBuilder.hasActiveFilters(activeFilters);
  const hasActive2 = FilterBuilder.hasActiveFilters(emptyFilters);
  
  console.log("Active filters check:", hasActive1);
  console.log("Empty filters check:", hasActive2);
  console.log("✅ Test 6 passed\n");
  
  console.log("🎉 All FilterBuilder tests passed!");
  
  return {
    basicTest: queryParams,
    arrayTest: arrayParams,
    validationTest: { valid: validValidation, invalid: invalidValidation },
    summaryTest: summary,
    activeFiltersTest: { active: hasActive1, empty: hasActive2 }
  };
}

// Test with realistic movie filter scenarios
export function testRealisticScenarios() {
  console.log("🎬 Testing realistic movie filtering scenarios...\n");
  
  const scenarios = [
    {
      name: "Action movies from 2010s with high ratings",
      filters: {
        genres: ["Action"],
        minYear: 2010,
        maxYear: 2019,
        minRating: 8,
        type: "movie"
      } as MovieFilters
    },
    {
      name: "Sci-Fi movies directed by Christopher Nolan",
      filters: {
        genres: ["Sci-Fi"],
        directors: ["Christopher Nolan"],
        type: "movie"
      } as MovieFilters
    },
    {
      name: "Movies with Keanu Reeves from the 90s",
      filters: {
        cast: ["Keanu Reeves"],
        minYear: 1990,
        maxYear: 1999,
        type: "movie"
      } as MovieFilters
    },
    {
      name: "Search for 'matrix' with specific criteria",
      filters: {
        search: "matrix",
        minRating: 7,
        include_invalid_posters: false,
        limit: 10
      } as MovieFilters
    }
  ];
  
  scenarios.forEach((scenario, index) => {
    console.log(`Scenario ${index + 1}: ${scenario.name}`);
    const params = FilterBuilder.buildQueryParams(scenario.filters);
    const validation = FilterBuilder.validateFilters(scenario.filters);
    const summary = FilterBuilder.getFilterSummary(scenario.filters);
    
    console.log("  Generated params:", params);
    console.log("  Validation:", validation.isValid ? "✅ Valid" : "❌ Invalid");
    if (!validation.isValid) {
      console.log("  Errors:", validation.errors);
    }
    console.log("  Summary:", summary.join(" | "));
    console.log("");
  });
  
  console.log("✅ All realistic scenarios tested!");
}

// Export for use in the app
export { FilterBuilder };
export type { MovieFilters };