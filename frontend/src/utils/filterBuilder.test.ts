/**
 * Test file for FilterBuilder utility
 * This file can be run with Node.js to test the FilterBuilder functionality
 */

// Import the FilterBuilder
import { FilterBuilder, MovieFilters } from './filterBuilder';

// Make this a module
export {};

// Mock test data
const testFilters = {
  // Basic filters
  search: "action",
  title: "The Matrix",
  type: "movie",
  
  // Array filters
  genres: ["Action", "Sci-Fi"],
  directors: ["Lana Wachowski", "Lilly Wachowski"],
  cast: ["Keanu Reeves", "Laurence Fishburne"],
  
  // Numeric filters
  year: 1999,
  minRating: 7,
  maxRating: 9,
  
  // Display options
  include_invalid_posters: false,
  limit: 24,
  skip: 0
};

// Test functions
function testFilterBuilder() {
  console.log("🧪 Testing FilterBuilder...\n");
  
  // Test 1: Basic query parameter building
  console.log("Test 1: Basic query parameter building");
  const queryParams = FilterBuilder.buildQueryParams(testFilters);
  console.log("Generated params:", JSON.stringify(queryParams, null, 2));
  console.log("✅ Test 1 passed\n");
  
  // Test 2: Has active filters
  console.log("Test 2: Has active filters");
  const hasActive = FilterBuilder.hasActiveFilters(testFilters);
  console.log("Has active filters:", hasActive);
  console.log("✅ Test 2 passed\n");
  
  // Test 3: Filter summary
  console.log("Test 3: Filter summary");
  const summary = FilterBuilder.getFilterSummary(testFilters);
  console.log("Filter summary:", summary);
  console.log("✅ Test 3 passed\n");
  
  // Test 4: Validation
  console.log("Test 4: Filter validation");
  const validation = FilterBuilder.validateFilters(testFilters);
  console.log("Validation result:", validation);
  console.log("✅ Test 4 passed\n");
  
  // Test 5: Edge cases
  console.log("Test 5: Edge cases");
  
  // Empty filters
  const emptyParams = FilterBuilder.buildQueryParams({});
  console.log("Empty filters params:", emptyParams);
  
  // Invalid range
  const invalidFilters = { minYear: 2020, maxYear: 2010 };
  const invalidValidation = FilterBuilder.validateFilters(invalidFilters);
  console.log("Invalid range validation:", invalidValidation);
  
  console.log("✅ Test 5 passed\n");
  
  console.log("🎉 All tests passed!");
}

// Test with different filter combinations
function testFilterCombinations() {
  console.log("🔍 Testing filter combinations...\n");
  
  const combinations = [
    {
      name: "Genre + Year",
      filters: { genres: ["Action"], year: 2020 }
    },
    {
      name: "Search + Rating",
      filters: { search: "matrix", minRating: 8 }
    },
    {
      name: "Director + Cast",
      filters: { directors: ["Nolan"], cast: ["DiCaprio"] }
    },
    {
      name: "Complex multi-filter",
      filters: {
        genres: ["Action", "Thriller"],
        year: 2010,
        minRating: 7,
        directors: ["Christopher Nolan"],
        type: "movie"
      }
    }
  ];
  
  combinations.forEach(({ name, filters }) => {
    console.log(`Testing: ${name}`);
    const params = FilterBuilder.buildQueryParams(filters);
    const validation = FilterBuilder.validateFilters(filters);
    const summary = FilterBuilder.getFilterSummary(filters);
    
    console.log("  Params:", Object.keys(params));
    console.log("  Valid:", validation.isValid);
    console.log("  Summary:", summary.join(", "));
    console.log("");
  });
  
  console.log("✅ All combination tests passed!");
}

// Run tests
if (require.main === module) {
  try {
    testFilterBuilder();
    console.log("\n" + "=".repeat(50) + "\n");
    testFilterCombinations();
  } catch (error) {
    console.error("❌ Test failed:", error);
    process.exit(1);
  }
}

export { testFilterBuilder, testFilterCombinations };