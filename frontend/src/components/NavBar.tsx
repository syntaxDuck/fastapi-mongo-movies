import React, { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import styles from "../styles/components/NavBar.module.css";

const NavBar: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/movies?search=${encodeURIComponent(searchQuery.trim())}`);
    }
    closeMenu(); // Close mobile menu after search
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
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <NavLink to="/" className={styles.brandLink}>
              MovieDB
            </NavLink>
          </motion.div>
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
              Search
            </button>
          </form>
        </div>

        <motion.button
          className={`${styles.navToggle} ${isMenuOpen ? styles.active : ""}`}
          onClick={toggleMenu}
          aria-label="Toggle navigation menu"
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
        >
          <span></span>
          <span></span>
          <span></span>
        </motion.button>

        <ul className={`${styles.navList} ${isMenuOpen ? styles.open : ""}`}>
          <li className={styles.navListItem}>
            <NavLink to="/" className={getNavLinkClassName} onClick={closeMenu}>
              Home
            </NavLink>
          </li>
          <li className={styles.navListItem}>
            <NavLink
              to="/movies"
              className={getNavLinkClassName}
              onClick={closeMenu}
            >
              Movies
            </NavLink>
          </li>
          <li className={styles.navListItem}>
            <NavLink
              to="/genres"
              className={getNavLinkClassName}
              onClick={closeMenu}
            >
              Genres
            </NavLink>
          </li>
          <li className={styles.navListItem}>
            <NavLink
              to="/top-rated"
              className={getNavLinkClassName}
              onClick={closeMenu}
            >
              Top Rated
            </NavLink>
          </li>
          <li className={styles.navListItem}>
            <NavLink
              to="/recent"
              className={getNavLinkClassName}
              onClick={closeMenu}
            >
              Recent
            </NavLink>
          </li>
          <li className={styles.navListItem}>
            <NavLink
              to="/about"
              className={getNavLinkClassName}
              onClick={closeMenu}
            >
              About
            </NavLink>
          </li>
          <li className={styles.navDivider}></li>
          <li className={styles.navListItem}>
            <NavLink
              to="/debug"
              className={getNavLinkClassName}
              onClick={closeMenu}
            >
              Debug
            </NavLink>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default NavBar;
