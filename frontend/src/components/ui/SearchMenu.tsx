import React, { useState, useEffect } from "react";
import { motion, AnimatePresence, Variants } from "framer-motion";
import { FilterBuilder, MovieFilters } from "../../utils/filterBuilder";

// Import utility components
import Input from "./Input";
import Select from "./Select";
import RangeInput from "./RangeInput";
import Button from "./Button";

import styles from "../../styles/components/ui/SearchMenu.module.css";

// SearchMenu component interface
export interface SearchMenuProps {
  initialFilters?: Partial<MovieFilters>;
  onSearch?: (filters: MovieFilters) => void;
  onFilterChange?: (filters: MovieFilters) => void;
  placeholder?: string;
  className?: string;
  id?: string;
  'aria-label'?: string;
}

// Framer Motion variants
const panelVariants: Variants = {
  collapsed: { 
    height: 0, 
    opacity: 0,
    transition: { 
      duration: 0.3, 
      ease: "easeInOut",
      when: "afterChildren"
    }
  },
  expanded: { 
    height: 'auto', 
    opacity: 1,
    transition: { 
      duration: 0.3, 
      ease: "easeInOut",
      when: "beforeChildren"
    }
  }
};

const toggleVariants: Variants = {
  collapsed: { rotate: 0 },
  expanded: { rotate: 180 }
};

const filterItemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.2, ease: "easeOut" }
  }
};

const filterContainerVariants: Variants = {
  hidden: {},
  visible: {
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.1
    }
  }
};

const errorVariants: Variants = {
  hidden: { opacity: 0, y: -10 },
  visible: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -10 }
};

// Genre options (can be fetched from API)
const genreOptions = [
  { value: 'Action', label: 'Action' },
  { value: 'Adventure', label: 'Adventure' },
  { value: 'Animation', label: 'Animation' },
  { value: 'Comedy', label: 'Comedy' },
  { value: 'Crime', label: 'Crime' },
  { value: 'Documentary', label: 'Documentary' },
  { value: 'Drama', label: 'Drama' },
  { value: 'Family', label: 'Family' },
  { value: 'Fantasy', label: 'Fantasy' },
  { value: 'History', label: 'History' },
  { value: 'Horror', label: 'Horror' },
  { value: 'Music', label: 'Music' },
  { value: 'Mystery', label: 'Mystery' },
  { value: 'Romance', label: 'Romance' },
  { value: 'Science Fiction', label: 'Science Fiction' },
  { value: 'TV Movie', label: 'TV Movie' },
  { value: 'Thriller', label: 'Thriller' },
  { value: 'War', label: 'War' },
  { value: 'Western', label: 'Western' }
];

const SearchMenu: React.FC<SearchMenuProps> = ({
  initialFilters = {},
  onSearch,
  onFilterChange,
  placeholder = "Search movies...",
  className,
  id,
  'aria-label': ariaLabel
}) => {
  // State management
  const [isExpanded, setIsExpanded] = useState(false);
  const [filters, setFilters] = useState<MovieFilters>(initialFilters);
  const [searchQuery, setSearchQuery] = useState('');
  const [validationErrors, setValidationErrors] = useState<string[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  // Sync state with prop if initialFilters changes
  // Using stringified version to avoid infinite loops from object identity
  const initialFiltersKey = JSON.stringify(initialFilters);
  useEffect(() => {
    setFilters(initialFilters);
  }, [initialFiltersKey]);

  // Filter change handler
  const handleFilterChange = (newFilters: Partial<MovieFilters>) => {
    const updatedFilters = { ...filters, ...newFilters };
    setFilters(updatedFilters);
    onFilterChange?.(updatedFilters);
    
    // Clear validation errors when filters change
    if (validationErrors.length > 0) {
      const validation = FilterBuilder.validateFilters(updatedFilters);
      setValidationErrors(validation.isValid ? [] : validation.errors);
    }
  };

  // Search handler with Framer Motion
  const handleSearch = async () => {
    if (isSearching) return;
    
    const searchFilters = { ...filters };
    if (searchQuery.trim()) {
      searchFilters.search = searchQuery.trim();
    }
    
    // Validate filters
    const validation = FilterBuilder.validateFilters(searchFilters);
    if (!validation.isValid) {
      setValidationErrors(validation.errors);
      return;
    }
    
    setValidationErrors([]);
    setIsSearching(true);
    
    try {
      await onSearch?.(searchFilters);
    } finally {
      setIsSearching(false);
    }
  };

  // Toggle handler
  const toggleExpanded = () => {
    setIsExpanded(!isExpanded);
  };

  // Clear filters handler
  const clearFilters = () => {
    setFilters(initialFilters);
    setSearchQuery('');
    setValidationErrors([]);
    onFilterChange?.(initialFilters);
  };

  // Check if filters are active
  const hasActiveFilters = FilterBuilder.hasActiveFilters(filters) || searchQuery.trim();

  // Handle search input key press
  const handleSearchKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <motion.div 
      className={`${styles.searchMenuContainer} ${className || ''}`}
      id={id}
      aria-label={ariaLabel}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      {/* Search Bar - Always Visible */}
      <motion.div 
        className={styles.searchBar}
        whileHover={{ scale: 1.01 }}
        transition={{ duration: 0.2 }}
      >
        <Input
          type="search"
          placeholder={placeholder}
          value={searchQuery}
          onChange={setSearchQuery}
          onClear={() => setSearchQuery('')}
          onKeyPress={handleSearchKeyPress}
          variant="search"
          className={styles.searchInput}
          aria-label="Search movies"
        />
        
        <motion.div className={styles.searchActions}>
          <Button
            onClick={handleSearch}
            variant="primary"
            className={styles.searchButton}
            disabled={isSearching}
            animation="scale"
          >
            {isSearching ? 'Searching...' : 'Search'}
          </Button>
          
          <motion.div className={styles.toggleWrapper}>
            <Button
              onClick={toggleExpanded}
              variant="secondary"
              className={styles.toggleButton}
              aria-expanded={isExpanded}
              ariaLabel={isExpanded ? 'Collapse filters' : 'Expand filters'}
              animation="scale"
            >
              <motion.span
                variants={toggleVariants}
                animate={isExpanded ? "expanded" : "collapsed"}
                transition={{ duration: 0.3 }}
              >
                {isExpanded ? '▲' : '▼'}
              </motion.span>
            </Button>
            
            {/* Active Filter Indicator */}
            {hasActiveFilters && (
              <motion.div 
                className={styles.activeIndicator}
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.2 }}
              />
            )}
          </motion.div>
        </motion.div>
      </motion.div>

      {/* Advanced Filters Panel - Expandable */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            className={styles.advancedPanel}
            variants={panelVariants}
            initial="collapsed"
            animate="expanded"
            exit="collapsed"
          >
            <motion.div 
              className={styles.panelContent}
              variants={filterContainerVariants}
              initial="hidden"
              animate="visible"
            >
              {/* Filter Categories Grid */}
              <motion.div 
                className={styles.filterGrid}
                variants={filterContainerVariants}
              >
                {/* Genre Multi-Select */}
                <motion.div className={styles.filterItem} variants={filterItemVariants}>
                  <Select
                    label="Genres"
                    options={genreOptions}
                    value={filters.genres || []}
                    onChange={(genres) => handleFilterChange({ genres: genres as string[] })}
                    placeholder="Select genres..."
                    multi={true}
                    variant="filter"
                  />
                </motion.div>

                {/* Year Range */}
                <motion.div className={styles.filterItem} variants={filterItemVariants}>
                  <RangeInput
                    label="Year Range"
                    min={1900}
                    max={new Date().getFullYear() + 5}
                    value={{ 
                      min: filters.minYear || 1900, 
                      max: filters.maxYear || new Date().getFullYear() + 5 
                    }}
                    onChange={(yearRange) => handleFilterChange({ 
                      minYear: yearRange.min, 
                      maxYear: yearRange.max 
                    })}
                    placeholder={{ min: "From", max: "To" }}
                  />
                </motion.div>

                {/* Rating Range */}
                <motion.div className={styles.filterItem} variants={filterItemVariants}>
                  <div className={styles.ratingFilter}>
                    <RangeInput
                      label="Rating Range"
                      min={0}
                      max={10}
                      value={{ 
                        min: filters.minRating || 0, 
                        max: filters.maxRating || 10 
                      }}
                      onChange={(ratingRange) => handleFilterChange({ 
                        minRating: ratingRange.min, 
                        maxRating: ratingRange.max 
                      })}
                      placeholder={{ min: "Min", max: "Max" }}
                    />
                    <Select
                      options={[
                        { value: 'imdb', label: 'IMDb' },
                        { value: 'tomatoes', label: 'Rotten Tomatoes' }
                      ]}
                      value={filters.ratingSource || 'imdb'}
                      onChange={(source) => handleFilterChange({ ratingSource: source as 'imdb' | 'tomatoes' })}
                      variant="filter"
                      size="sm"
                      aria-label="Rating source"
                    />
                  </div>
                </motion.div>

                {/* Sort Options */}
                <motion.div className={styles.filterItem} variants={filterItemVariants}>
                  <div className={styles.sortOptions}>
                    <Select
                      label="Sort By"
                      options={[
                        { value: 'title', label: 'Title' },
                        { value: 'year', label: 'Year' },
                        { value: 'imdb.rating', label: 'IMDb Rating' },
                        { value: 'tomatoes.viewer.rating', label: 'Audience Score' }
                      ]}
                      value={filters.sort_by || 'title'}
                      onChange={(sortBy) => handleFilterChange({ sort_by: sortBy as string })}
                      placeholder="Sort by..."
                      variant="filter"
                    />
                    <Select
                      options={[
                        { value: 'asc', label: 'Ascending' },
                        { value: 'desc', label: 'Descending' }
                      ]}
                      value={filters.sort_order || 'asc'}
                      onChange={(sortOrder) => handleFilterChange({ sort_order: sortOrder as 'asc' | 'desc' })}
                      variant="filter"
                      size="sm"
                      aria-label="Sort order"
                    />
                  </div>
                </motion.div>
              </motion.div>

              {/* Action Buttons */}
              <motion.div 
                className={styles.panelActions}
                variants={filterItemVariants}
              >
                <Button
                  onClick={clearFilters}
                  variant="secondary"
                  className={styles.clearButton}
                  animation="scale"
                >
                  Clear All
                </Button>
                <Button
                  onClick={handleSearch}
                  variant="primary"
                  className={styles.applyButton}
                  disabled={isSearching}
                  animation="scale"
                >
                  {isSearching ? 'Applying...' : 'Apply Filters'}
                </Button>
              </motion.div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Validation Errors */}
      <AnimatePresence>
        {validationErrors.length > 0 && (
          <motion.div
            className={styles.validationErrors}
            variants={errorVariants}
            initial="hidden"
            animate="visible"
            exit="exit"
          >
            {validationErrors.slice(0, 3).map((error, index) => (
              <motion.div 
                key={index} 
                className={styles.errorMessage}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                ⚠️ {error}
              </motion.div>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
};

export default SearchMenu;