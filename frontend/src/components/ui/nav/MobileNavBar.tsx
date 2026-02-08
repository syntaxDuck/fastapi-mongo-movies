import React, { useState } from 'react'
import { NavLink } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'

interface MobileNavBarProps {
  styles: any,
  links: { name: string, link: string }[]
}

const MobileNavBar: React.FC<MobileNavBarProps> = ({ styles, links }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const mobileMenuVariants = {
    closed: {
      opacity: 0,
      height: 0,
      y: -10
    },
    open: {
      opacity: 1,
      height: "auto",
      y: 0
    }
  };

  const navLinkVariants = {
    closed: { opacity: 0, x: -20 },
    open: { opacity: 1, x: 0 }
  };

  const navLinkHoverVariants = {
    hover: {
      y: -1,
      backgroundColor: "var(--bg-hover)",
      color: "var(--text-primary)"
    }
  };

  const hamburgerVariants = {
    closed: {
      span1: { rotate: 0, y: 6 },
      span2: { opacity: 1 },
      span3: { rotate: 0, y: -6 }
    },
    open: {
      span1: { rotate: 45, y: 3 },
      span2: { opacity: 0 },
      span3: { rotate: -45, y: 3 }
    }
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  const getNavLinkClassName = ({ isActive }: { isActive: boolean }) =>
    `${styles.navLink} ${isActive ? styles.active : ""}`;

  return (
    <>
      <motion.button
        className={`${styles.navToggle} ${isMenuOpen ? styles.active : ""}`}
        onClick={toggleMenu}
        aria-label="Toggle navigation menu"
        whileHover={{ scale: 1.1, backgroundColor: "var(--bg-hover)" }}
        whileTap={{ scale: 0.9 }}
      >
        <motion.span
          animate={isMenuOpen ? hamburgerVariants.open.span1 : hamburgerVariants.closed.span1}
          transition={{ duration: 0.3, ease: "easeInOut" }}
        />
        <motion.span
          animate={isMenuOpen ? hamburgerVariants.open.span2 : hamburgerVariants.closed.span2}
          transition={{ duration: 0.3, ease: "easeInOut" }}
        />
        <motion.span
          animate={isMenuOpen ? hamburgerVariants.open.span3 : hamburgerVariants.closed.span3}
          transition={{ duration: 0.3, ease: "easeInOut" }}
        />

      </motion.button>
      <AnimatePresence>
        {isMenuOpen && (
          <motion.ul
            className={`${styles.navList} ${styles.open}`}
            variants={mobileMenuVariants}
            initial="closed"
            animate="open"
            exit="closed"
            transition={{ duration: 0.3, ease: "easeInOut" }}
          >
            {links.map((element, _) => <motion.li className={styles.navListItem} variants={navLinkVariants}>
              <motion.div whileHover="hover" variants={navLinkHoverVariants} transition={{ duration: 0.2, ease: "easeOut" }}>
                <NavLink to={element.link} className={getNavLinkClassName} onClick={closeMenu}>
                  {element.name}
                </NavLink>
              </motion.div>
            </motion.li>)}
            <motion.li className={styles.navDivider} variants={navLinkVariants}></motion.li>
            <motion.li className={styles.navListItem} variants={navLinkVariants}>
              <motion.div
                whileHover="hover"
                variants={navLinkHoverVariants}
                transition={{ duration: 0.2, ease: "easeOut" }}
              >
                <NavLink
                  to="/debug"
                  className={getNavLinkClassName}
                  onClick={closeMenu}
                >
                  Debug
                </NavLink>
              </motion.div>
            </motion.li>
          </motion.ul>
        )}
      </AnimatePresence>
    </>

  )
}

export default MobileNavBar;
