import React, { useState, useEffect } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import DesktopNavBar from "./DesktopNavBar";
import MobileNavBar from "./MobileNavBar";
import styles from "../../../styles/components/ui/NavBar.module.css";

const navLinks: { name: string, link: string }[] = [
  { name: "Movies", link: "/movies" },
  { name: "Genres", link: "/genres" },
  { name: "Top Rated", link: "/top-rated" },
  { name: "Recent", link: "/recent" },
  { name: "About", link: "/about" },
]

//BUG: When clicking to laod more movies the search parameter is no longer respected
const NavBar: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [isMobile, setIsMobile] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const navBarVariants = {
    initial: { opacity: 0, y: -20 },
    animate: { opacity: 1, y: 0 }
  };

  const brandVariants = {
    hover: { scale: 1.05 }
  };

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/movies?search=${encodeURIComponent(searchQuery.trim())}`);
    }
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
              type="text"
              placeholder="Search movies..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className={styles.searchInput}
              whileFocus={{
                borderColor: "var(--primary-500)",
                boxShadow: "0 0 0 3px rgba(59, 130, 246, 0.1)",
                backgroundColor: "var(--bg-primary)"
              }}
              transition={{ duration: 0.2 }}
            />
            <motion.button
              type="submit"
              className={styles.searchBtn}
              whileHover={{
                color: "var(--text-primary)",
                backgroundColor: "var(--bg-hover)"
              }}
              transition={{ duration: 0.2 }}
            >
              Search
            </motion.button>
          </form>
        </div>

        {!isMobile && (
          <DesktopNavBar styles={styles} links={navLinks} />
        )}

        {isMobile && (
          <MobileNavBar styles={styles} links={navLinks} />
        )}
      </div>
    </motion.nav>
  );
};

export default NavBar;
