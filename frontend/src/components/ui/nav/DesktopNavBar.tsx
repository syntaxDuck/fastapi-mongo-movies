import React from 'react'
import { motion, Variants } from 'framer-motion'
import { NavLink } from 'react-router-dom'

interface DesktopNavBarProps {
  styles: any,
  links: { name: string, link: string }[],

}

const DesktopNavBar: React.FC<DesktopNavBarProps> = ({ styles, links }) => {

  const navVariants: Variants = {
    hidden: {
      transition: {
        staggerChildren: 0.07
      }
    },
    visible: {
      transition: {
        staggerChildren: 0.07,
        delayChildren: 0.2
      }
    }
  }

  const navItemVariants: Variants = {
    hidden: {
      x: -100,
      opacity: 0
    },
    visible: {
      x: 0,
      opacity: 1,
      transition: {
        type: "spring",
        stiffness: 350,
        damping: 28
      }
    },
  };

  const linkVariants: Variants = {
    hover: {
      scale: 1.05,
      y: -2,
      backgroundColor: "var(--bg-hover)",
      color: "var(--text-primary)",
    },
    tap: {
      scale: 0.95,
    }
  }

  const getNavLinkClassName = ({ isActive }: { isActive: boolean }) =>
    `${styles.navLink} ${isActive ? styles.active : ""}`;

  return (
    <motion.ul className={styles.navList} variants={navVariants} initial="hidden" animate="visible">
      {links.map((element, index) =>
        <motion.li key={index} className={styles.navListItem} variants={navItemVariants}>
          <motion.div className={styles.navListItem} variants={linkVariants} whileHover="hover"
            whileTap="tag">
            <NavLink to={element.link} className={getNavLinkClassName}>
              {element.name}
            </NavLink>
          </motion.div>
        </motion.li>)
      }
    </motion.ul >
  )
}

export default DesktopNavBar;
