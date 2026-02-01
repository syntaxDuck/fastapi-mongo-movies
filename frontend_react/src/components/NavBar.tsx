import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import './NavBar.css';

const NavBar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement search functionality
    console.log('Searching for:', searchQuery);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  return (
    <nav className="nav-bar">
      <div className="nav-container">
        <div className="nav-brand">
          <NavLink to="/" className="brand-link">
            🎬 MovieDB
          </NavLink>
        </div>

        <div className="nav-search">
          <form onSubmit={handleSearch} className="search-form">
            <input
              type="text"
              placeholder="Search movies..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="search-input"
            />
            <button type="submit" className="search-btn">
              🔍
            </button>
          </form>
        </div>

        <button
          className={`nav-toggle ${isMenuOpen ? 'active' : ''}`}
          onClick={toggleMenu}
          aria-label="Toggle navigation menu"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <ul className={`nav-list ${isMenuOpen ? 'open' : ''}`}>
          <li>
            <NavLink 
              to="/" 
              className={({ isActive }) => isActive ? 'active' : ''}
              onClick={closeMenu}
            >
              🏠 Home
            </NavLink>
          </li>
          <li>
            <NavLink 
              to="/movies" 
              className={({ isActive }) => isActive ? 'active' : ''}
              onClick={closeMenu}
            >
              🎭 Movies
            </NavLink>
          </li>
          <li>
            <NavLink 
              to="/genres" 
              className={({ isActive }) => isActive ? 'active' : ''}
              onClick={closeMenu}
            >
              🎨 Genres
            </NavLink>
          </li>
          <li>
            <NavLink 
              to="/directors" 
              className={({ isActive }) => isActive ? 'active' : ''}
              onClick={closeMenu}
            >
              🎬 Directors
            </NavLink>
          </li>
          <li>
            <NavLink 
              to="/top-rated" 
              className={({ isActive }) => isActive ? 'active' : ''}
              onClick={closeMenu}
            >
              ⭐ Top Rated
            </NavLink>
          </li>
          <li>
            <NavLink 
              to="/recent" 
              className={({ isActive }) => isActive ? 'active' : ''}
              onClick={closeMenu}
            >
              🆕 Recent
            </NavLink>
          </li>
          <li>
            <NavLink 
              to="/about" 
              className={({ isActive }) => isActive ? 'active' : ''}
              onClick={closeMenu}
            >
              ℹ️ About
            </NavLink>
          </li>
          <li className="nav-divider"></li>
          <li>
            <NavLink 
              to="/debug" 
              className={({ isActive }) => isActive ? 'active' : ''}
              onClick={closeMenu}
            >
              🐛 Debug
            </NavLink>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default NavBar;