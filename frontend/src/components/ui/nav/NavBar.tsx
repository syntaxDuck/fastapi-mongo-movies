import React, { useState, useEffect, useRef } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import DesktopNavBar from "./DesktopNavBar";
import MobileNavBar from "./MobileNavBar";
import styles from "../../../styles/components/ui/NavBar.module.css";

const navLinks: { name: string; link: string }[] = [
  { name: "Movies", link: "/movies" },
  { name: "Genres", link: "/genres" },
  { name: "Top Rated", link: "/top-rated" },
  { name: "Recent", link: "/recent" },
  { name: "About", link: "/about" },
];

//BUG: When clicking to laod more movies the search parameter is no longer respected
const NavBar: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [isMobile, setIsMobile] = useState(false);
  const navigate = useNavigate();
  const searchInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    checkMobile();
    window.addEventListener("resize", checkMobile);
    return () => window.removeEventListener("resize", checkMobile);
  }, []);

  const navBarVariants = {
    initial: { opacity: 0, y: -20 },
    animate: { opacity: 1, y: 0 },
  };

  const brandVariants = {
    hover: { scale: 1.05 },
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/movies?search=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  const handleClear = () => {
    setSearchQuery("");
    searchInputRef.current?.focus();
  };

  return (
    <motion.nav
      className={styles.navBar}
      variants={navBarVariants}
      initial="initial"
      animate="animate"
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      <div className={styles.navContainer}>
        <div className={styles.navBrand}>
          <motion.div
            variants={brandVariants}
            whileHover="hover"
            whileTap={{ scale: 0.95 }}
            transition={{ duration: 0.2, ease: "easeOut" }}
          >
            <NavLink to="/" className={styles.brandLink}>
              MovieDB
            </NavLink>
          </motion.div>
        </div>

        <div className={styles.navSearch}>
          <form onSubmit={handleSearch} className={styles.searchForm}>
            <motion.input
              ref={searchInputRef}
              type="text"
              placeholder="Search movies..."
              aria-label="Search movies"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className={styles.searchInput}
              whileFocus={{
                borderColor: "var(--primary-500)",
                boxShadow: "0 0 0 3px rgba(59, 130, 246, 0.1)",
                backgroundColor: "var(--bg-primary)",
              }}
              transition={{ duration: 0.2 }}
            />
            <AnimatePresence>
              {searchQuery && (
                <motion.button
                  type="button"
                  className={styles.clearBtn}
                  onClick={handleClear}
                  aria-label="Clear search"
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.8 }}
                  whileHover={{ color: "var(--text-primary)" }}
                  transition={{ duration: 0.2 }}
                >
                  &times;
                </motion.button>
              )}
            </AnimatePresence>
            <motion.button
              type="submit"
              className={styles.searchBtn}
              aria-label="Submit search"
              whileHover={{
                color: "var(--text-primary)",
                backgroundColor: "var(--bg-hover)",
              }}
              transition={{ duration: 0.2 }}
            >
              🔍
            </motion.button>
          </form>
        </div>

        {!isMobile && <DesktopNavBar styles={styles} links={navLinks} />}

        {isMobile && <MobileNavBar styles={styles} links={navLinks} />}
      </div>
    </motion.nav>
  );
};

export default NavBar;
