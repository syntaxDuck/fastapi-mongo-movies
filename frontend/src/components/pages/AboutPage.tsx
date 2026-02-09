import React from "react";
import { motion, Variants } from "framer-motion";
import styles from "../../styles/components/pages/AboutPage.module.css";

// Reusable components
import FeatureCard from "./FeatureCard";
import TechStackCard from "./TechStackCard";
import StatCounter from "./StatCounter";

const AboutPage: React.FC = () => {
  const pageVariants: Variants = {
    initial: { opacity: 0, y: 20 },
    animate: {
      opacity: 1,
      y: 0
    }
  };

  const sectionVariants: Variants = {
    initial: { opacity: 0, y: 30 },
    animate: {
      opacity: 1,
      y: 0
    }
  };

  const features = [
    {
      icon: "🎬",
      title: "Extensive Collection",
      description: "Explore thousands of movies from the MongoDB sample_mflix dataset spanning decades of cinema."
    },
    {
      icon: "🔍",
      title: "Smart Search",
      description: "Powerful search functionality with filtering by genre, year, rating, and more to find exactly what you want."
    },
    {
      icon: "⚡",
      title: "Lightning Fast",
      description: "Built with FastAPI and React for optimal performance, delivering instant responses and smooth interactions."
    },
    {
      icon: "🏗️",
      title: "Clean Architecture",
      description: "Professional code structure with separation of concerns, making it maintainable and scalable."
    }
  ];

  const techStack = [
    {
      name: "FastAPI",
      category: "Backend",
      description: "Modern, fast web framework for building APIs with Python",
      color: "#009688"
    },
    {
      name: "MongoDB",
      category: "Database",
      description: "NoSQL database with flexible schema and powerful querying",
      color: "#4DB33D"
    },
    {
      name: "React",
      category: "Frontend",
      description: "Component-based UI library for building interactive interfaces",
      color: "#61DAFB"
    },
    {
      name: "TypeScript",
      category: "Language",
      description: "Typed JavaScript for better code quality and developer experience",
      color: "#3178C6"
    }
  ];

  const stats = [
    { number: 23000, label: "Movies", suffix: "+" },
    { number: 1950, label: "Years Covered", suffix: "s" },
    { number: 20, label: "Genres", suffix: "+" },
    { number: 100, label: "Performance", suffix: "%" }
  ];

  return (
    <motion.div
      className={styles.aboutContainer}
      variants={pageVariants}
      initial="initial"
      animate="animate"
      transition={{ duration: 0.6, ease: "easeOut", staggerChildren: 0.2 }}
    >
      {/* Hero Section */}
      <motion.section
        className={styles.heroSection}
        variants={sectionVariants}
        transition={{ duration: 0.5, ease: "easeOut" }}
      >
        <div className={styles.heroContent}>
          <h1 className={styles.heroTitle}>
            About MovieDB
          </h1>
          <p className={styles.heroSubtitle}>
            A modern, full-stack movie database application showcasing clean architecture,
            powerful search capabilities, and an exceptional user experience.
          </p>
          <div className={styles.heroActions}>
            <a href="/movies" className={styles.btnPrimary}>
              Browse Movies
            </a>
            <a href="/genres" className={styles.btnSecondary}>
              Explore Genres
            </a>
          </div>
        </div>
      </motion.section>

      {/* Project Overview */}
      <motion.section
        className={styles.overviewSection}
        variants={sectionVariants}
      >
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Project Overview</h2>
          <p className={styles.sectionSubtitle}>
            FastAPI MongoDB Movies demonstrates professional web development with modern technologies
          </p>
        </div>
        <div className={styles.overviewGrid}>
          <div className={styles.overviewCard}>
            <h3>Modern Stack</h3>
            <p>Built with cutting-edge technologies including FastAPI, MongoDB, React, and TypeScript for optimal performance and developer experience.</p>
          </div>
          <div className={styles.overviewCard}>
            <h3>Clean Code</h3>
            <p>Follows industry best practices with clean architecture, comprehensive testing, and maintainable code structure.</p>
          </div>
          <div className={styles.overviewCard}>
            <h3>User Focused</h3>
            <p>Designed with users in mind, featuring intuitive navigation, powerful search, and responsive design for all devices.</p>
          </div>
        </div>
      </motion.section>

      {/* Key Features */}
      <motion.section
        className={styles.featuresSection}
        variants={sectionVariants}
      >
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Key Features</h2>
          <p className={styles.sectionSubtitle}>
            Discover what makes this application special
          </p>
        </div>
        <div className={styles.featuresGrid}>
          {features.map((feature, index) => (
            <FeatureCard
              key={index}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
              index={index}
            />
          ))}
        </div>
      </motion.section>

      {/* Technical Architecture */}
      <motion.section
        className={styles.architectureSection}
        variants={sectionVariants}
      >
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Technical Architecture</h2>
          <p className={styles.sectionSubtitle}>
            Built with modern technologies and best practices
          </p>
        </div>
        <div className={styles.architectureGrid}>
          <div className={styles.architectureVisual}>
            <div className={styles.architectureLayer}>
              <h4>Frontend</h4>
              <p>React + TypeScript + CSS Modules</p>
            </div>
            <div className={styles.architectureLayer}>
              <h4>API</h4>
              <p>FastAPI + Pydantic + AsyncIO</p>
            </div>
            <div className={styles.architectureLayer}>
              <h4>Database</h4>
              <p>MongoDB + Motor ODM</p>
            </div>
          </div>
          <div className={styles.architectureDescription}>
            <h3>Clean Architecture Pattern</h3>
            <p>Our application follows the clean architecture principle with clear separation between API, service, and repository layers. This ensures maintainability, testability, and scalability.</p>
            <ul className={styles.architectureList}>
              <li>API Layer: HTTP request handling and routing</li>
              <li>Service Layer: Business logic and orchestration</li>
              <li>Repository Layer: Data access abstraction</li>
              <li>Core Layer: Database configuration and utilities</li>
            </ul>
          </div>
        </div>
      </motion.section>

      {/* Technology Stack */}
      <motion.section
        className={styles.techStackSection}
        variants={sectionVariants}
      >
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Technology Stack</h2>
          <p className={styles.sectionSubtitle}>
            Powered by industry-leading technologies
          </p>
        </div>
        <div className={styles.techStackGrid}>
          {techStack.map((tech, index) => (
            <TechStackCard
              key={index}
              name={tech.name}
              category={tech.category}
              description={tech.description}
              color={tech.color}
              index={index}
            />
          ))}
        </div>
      </motion.section>

      {/* Database Showcase */}
      <motion.section
        className={styles.databaseSection}
        variants={sectionVariants}
      >
        <div className={styles.sectionHeader}>
          <h2 className={styles.sectionTitle}>Database Showcase</h2>
          <p className={styles.sectionSubtitle}>
            Powered by the MongoDB sample_mflix dataset
          </p>
        </div>
        <div className={styles.statsGrid}>
          {stats.map((stat, index) => (
            <StatCounter
              key={index}
              number={stat.number}
              label={stat.label}
              suffix={stat.suffix}
              index={index}
            />
          ))}
        </div>
        <div className={styles.databaseInfo}>
          <div className={styles.databaseCard}>
            <h3>Rich Movie Data</h3>
            <p>Comprehensive information including cast, crew, plot, ratings, and metadata for thousands of films.</p>
          </div>
          <div className={styles.databaseCard}>
            <h3>Multiple Rating Systems</h3>
            <p>IMDb and Rotten Tomatoes ratings help users discover quality content and make informed choices.</p>
          </div>
          <div className={styles.databaseCard}>
            <h3>Advanced Search</h3>
            <p>Full-text search, filtering by genre, year, country, and more with MongoDB's powerful query capabilities.</p>
          </div>
        </div>
      </motion.section>

      {/* Call to Action */}
      <motion.section
        className={styles.ctaSection}
        variants={sectionVariants}
      >
        <div className={styles.ctaContent}>
          <h2 className={styles.ctaTitle}>Start Exploring</h2>
          <p className={styles.ctaSubtitle}>
            Dive into our extensive movie collection and discover your next favorite film
          </p>
          <div className={styles.ctaActions}>
            <a href="/movies" className={styles.btnPrimary}>
              Browse All Movies
            </a>
            <a href="/top-rated" className={styles.btnSecondary}>
              Top Rated Films
            </a>
          </div>
        </div>
      </motion.section>
    </motion.div>
  );
};

export default AboutPage;
