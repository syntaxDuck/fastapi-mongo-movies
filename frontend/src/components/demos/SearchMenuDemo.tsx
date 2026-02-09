import React, { useState } from 'react';
import { SearchMenu } from '../ui';
import { FilterBuilder, MovieFilters } from '../../utils/filterBuilder';

/**
 * SearchMenuDemo - Demo component to showcase SearchMenu functionality
 * This demonstrates how to use the SearchMenu component with different configurations
 */
const SearchMenuDemo: React.FC = () => {
  // State for managing filters
  const [currentFilters, setCurrentFilters] = useState<MovieFilters>({});
  const [searchHistory, setSearchHistory] = useState<MovieFilters[]>([]);

  // Handle search
  const handleSearch = (filters: MovieFilters) => {
    console.log('Searching with filters:', filters);
    
    // Build query parameters for API call
    const queryParams = FilterBuilder.buildQueryParams(filters);
    console.log('Query parameters:', queryParams);
    
    // Add to search history
    setSearchHistory(prev => [...prev.slice(-4), filters]);
    
    // Here you would typically make an API call
    // const results = await movieService.fetchMovies(queryParams);
  };

  // Handle filter change (optional - for real-time updates)
  const handleFilterChange = (filters: MovieFilters) => {
    console.log('Filters changed:', filters);
    setCurrentFilters(filters);
  };

  // Get filter summary for display
  const getFilterSummary = (filters: MovieFilters) => {
    const summary = FilterBuilder.getFilterSummary(filters);
    return summary.length > 0 ? summary.join(', ') : 'No filters applied';
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>SearchMenu Component Demo</h1>
      
      {/* Basic SearchMenu */}
      <section style={{ marginBottom: '40px' }}>
        <h2>Basic SearchMenu</h2>
        <SearchMenu
          onSearch={handleSearch}
          onFilterChange={handleFilterChange}
          placeholder="Search for movies..."
        />
      </section>

      {/* SearchMenu with initial filters */}
      <section style={{ marginBottom: '40px' }}>
        <h2>SearchMenu with Initial Filters</h2>
        <SearchMenu
          initialFilters={{ minRating: 7, genres: ['Action', 'Drama'] }}
          onSearch={handleSearch}
          onFilterChange={handleFilterChange}
          placeholder="Search filtered movies..."
        />
      </section>

      {/* Current Filters Display */}
      <section style={{ marginBottom: '40px' }}>
        <h2>Current Filters</h2>
        <div style={{ 
          padding: '15px', 
          background: '#f5f5f5', 
          borderRadius: '8px',
          fontFamily: 'monospace',
          fontSize: '14px'
        }}>
          <div><strong>Filter Summary:</strong> {getFilterSummary(currentFilters)}</div>
          <div style={{ marginTop: '10px' }}>
            <strong>Raw Filters:</strong>
            <pre style={{ margin: '5px 0', fontSize: '12px' }}>
              {JSON.stringify(currentFilters, null, 2)}
            </pre>
          </div>
        </div>
      </section>

      {/* Search History */}
      <section style={{ marginBottom: '40px' }}>
        <h2>Search History</h2>
        {searchHistory.length === 0 ? (
          <p>No searches yet. Try searching above!</p>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {searchHistory.map((filters, index) => (
              <div 
                key={index}
                style={{ 
                  padding: '10px', 
                  background: '#e9ecef', 
                  borderRadius: '6px',
                  fontSize: '14px'
                }}
              >
                <div><strong>Search {index + 1}:</strong> {getFilterSummary(filters)}</div>
                <div style={{ fontSize: '12px', opacity: 0.7 }}>
                  {JSON.stringify(FilterBuilder.buildQueryParams(filters))}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>

      {/* Usage Examples */}
      <section>
        <h2>Usage Examples</h2>
        <div style={{ 
          padding: '15px', 
          background: '#f8f9fa', 
          borderRadius: '8px',
          fontSize: '14px',
          lineHeight: '1.6'
        }}>
          <h3>Basic Usage:</h3>
          <pre style={{ background: '#fff', padding: '10px', borderRadius: '4px' }}>
{`import { SearchMenu } from './components/ui';

<SearchMenu
  onSearch={(filters) => {
    // Handle search with filters
    console.log(filters);
  }}
  placeholder="Search movies..."
/>`}
          </pre>

          <h3>Advanced Usage:</h3>
          <pre style={{ background: '#fff', padding: '10px', borderRadius: '4px' }}>
{`import { SearchMenu, MovieFilters } from './components/ui';
import { FilterBuilder } from './utils/filterBuilder';

const [filters, setFilters] = useState<MovieFilters>({});

<SearchMenu
  initialFilters={{ minRating: 7 }}
  onSearch={(filters) => {
    const queryParams = FilterBuilder.buildQueryParams(filters);
    // Make API call with queryParams
  }}
  onFilterChange={setFilters}
  placeholder="Search movies..."
/>`}
          </pre>

          <h3>Features:</h3>
          <ul>
            <li>✅ Toggle between simple and advanced search modes</li>
            <li>✅ Filter persistence across expand/collapse</li>
            <li>✅ Real-time validation with error display</li>
            <li>✅ Multi-select genre filtering</li>
            <li>✅ Year and rating range inputs</li>
            <li>✅ Sort options (by title, year, rating)</li>
            <li>✅ Framer Motion animations (0.3s transitions)</li>
            <li>✅ Responsive design for mobile/tablet</li>
            <li>✅ Accessibility support (ARIA labels, keyboard navigation)</li>
            <li>✅ Generic utility components (Input, Select, RangeInput)</li>
          </ul>
        </div>
      </section>
    </div>
  );
};

export default SearchMenuDemo;