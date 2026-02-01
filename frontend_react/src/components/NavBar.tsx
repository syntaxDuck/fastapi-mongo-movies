import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import styles from "../styles/components/NavBar.module.css";

const NavBar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement search functionality
    console.log("Searching for:", searchQuery);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  const getNavLinkClassName = ({ isActive }: { isActive: boolean }) =>
    `${styles.navLink} ${isActive ? styles.active : ""}`;

  return (
    <nav className={styles.navBar}>
      <div className={styles.navContainer}>
        <div className={styles.navBrand}>
          <NavLink to="/" className={styles.brandLink}>
            🎬 MovieDB
          </NavLink>
        </div>

        <div className={styles.navSearch}>
          <form onSubmit={handleSearch} className={styles.searchForm}>
            <input
              type="text"
              placeholder="Search movies..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className={styles.searchInput}
            />
            <button type="submit" className={styles.searchBtn}>
              🔍
            </button>
          </form>
        </div>

        <button
          className={`${styles.navToggle} ${isMenuOpen ? styles.active : ""}`}
          onClick={toggleMenu}
          aria-label="Toggle navigation menu"
        >
          <span></span>
          <span></span>
          <span></span>
        </button>

        <ul className={`${styles.navList} ${isMenuOpen ? styles.open : ""}`}>
          <li className={styles.navListItem}>
            <NavLink to="/" className={getNavLinkClassName} onClick={closeMenu}>
              🏠 Home
            </NavLink>
          </li>
          <li className={styles.navListItem}>
            <NavLink
              to="/movies"
              className={getNavLinkClassName}
              onClick={closeMenu}
            >
              🎭 Movies
            </NavLink>
          </li>
          <li className={styles.navListItem}>
            <NavLink
              to="/genres"
              className={getNavLinkClassName}
              onClick={closeMenu}
            >
              🎨 Genres
            </NavLink>
          </li>
          <li className={styles.navListItem}>
            <NavLink
              to="/directors"
              className={getNavLinkClassName}
              onClick={closeMenu}
            >
              🎬 Directors
            </NavLink>
          </li>
          <li className={styles.navListItem}>
            <NavLink
              to="/top-rated"
              className={getNavLinkClassName}
              onClick={closeMenu}
            >
              ⭐ Top Rated
            </NavLink>
          </li>
          <li className={styles.navListItem}>
            <NavLink
              to="/recent"
              className={getNavLinkClassName}
              onClick={closeMenu}
            >
              🆕 Recent
            </NavLink>
          </li>
          <li className={styles.navListItem}>
            <NavLink
              to="/about"
              className={getNavLinkClassName}
              onClick={closeMenu}
            >
              ℹ️ About
            </NavLink>
          </li>
          <li className={styles.navDivider}></li>
          <li className={styles.navListItem}>
            <NavLink
              to="/debug"
              className={getNavLinkClassName}
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
