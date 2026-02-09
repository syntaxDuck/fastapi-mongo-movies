import React from 'react';
import { SearchMenu } from '../ui';
import { FilterBuilder, MovieFilters } from '../../utils/filterBuilder';

/**
 * Simple test page to verify SearchMenu component functionality
 */
const SearchMenuTest: React.FC = () => {
  const handleSearch = (filters: MovieFilters) => {
    console.log('Search triggered with filters:', filters);
    
    // Build query parameters
    const queryParams = FilterBuilder.buildQueryParams(filters);
    console.log('Query parameters:', queryParams);
    
    // Show alert for testing
    alert(`Search triggered!\nFilters: ${JSON.stringify(filters, null, 2)}\nQuery params: ${JSON.stringify(queryParams, null, 2)}`);
  };

  const handleFilterChange = (filters: MovieFilters) => {
    console.log('Filters changed:', filters);
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>SearchMenu Component Test</h1>
      <p>This page tests the SearchMenu component with various configurations.</p>
      
      <div style={{ marginBottom: '40px' }}>
        <h2>Basic SearchMenu</h2>
        <SearchMenu
          onSearch={handleSearch}
          onFilterChange={handleFilterChange}
          placeholder="Search for movies..."
        />
      </div>

      <div style={{ marginBottom: '40px' }}>
        <h2>SearchMenu with Initial Filters</h2>
        <SearchMenu
          initialFilters={{ minRating: 7, genres: ['Action'] }}
          onSearch={handleSearch}
          onFilterChange={handleFilterChange}
          placeholder="Search filtered movies..."
        />
      </div>

      <div style={{ marginBottom: '40px' }}>
        <h2>Test Instructions</h2>
        <ol>
          <li>Test the basic search functionality by typing in the search bar and clicking "Search"</li>
          <li>Click the toggle button (▼) to expand the advanced filters panel</li>
          <li>Test various filter combinations:
            <ul>
              <li>Select multiple genres</li>
              <li>Set year range</li>
              <li>Set rating range</li>
              <li>Change sort options</li>
            </ul>
          </li>
          <li>Test the "Clear All" button to reset filters</li>
          <li>Test the "Apply Filters" button to search with advanced filters</li>
          <li>Test validation by setting invalid ranges (e.g., min year &gt; max year)</li>
          <li>Test keyboard navigation and accessibility</li>
        </ol>
      </div>

      <div style={{ marginBottom: '40px' }}>
        <h2>Expected Behavior</h2>
        <ul>
          <li>✅ Component starts collapsed (simple search bar only)</li>
          <li>✅ Toggle button rotates (▼ ↔ ▲) when clicked</li>
          <li>✅ Advanced panel expands with smooth animation (0.3s)</li>
          <li>✅ Filters persist when panel is collapsed</li>
          <li>✅ Active filter indicator appears when filters are applied</li>
          <li>✅ Validation errors appear for invalid filter combinations</li>
          <li>✅ Search works from both collapsed and expanded states</li>
          <li>✅ Responsive design works on mobile devices</li>
        </ul>
      </div>
    </div>
  );
};

export default SearchMenuTest;