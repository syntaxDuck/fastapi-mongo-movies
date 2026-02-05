import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import NavBar from "./components/NavBar";
import MovieList from "./components/movies/MovieList";
import MovieDetails from "./components/movies/MovieDetails";

import GenresView from "./components/genres/GenresView";
import GenreMoviesView from "./components/genres/GenreMoviesView";
import ApiDebug from "./components/util/ApiDebug";
import MovieView from "./components/views/MovieView";
import HeroPage from "./components/HeroPage";
import DevelopmentRoutes from "./components/dev/DevelopmentRoutes";
import SpinnerTest from "./components/dev/SpinnerTest";

// Import consolidated stylesheet
import "./styles/index.css";

// Page transition variants
const pageVariants = {
  initial: {
    opacity: 0,
    y: 20,
    scale: 0.98,
  },
  in: {
    opacity: 1,
    y: 0,
    scale: 1,
  },
  out: {
    opacity: 0,
    y: -20,
    scale: 0.98,
  },
};

const pageTransition = {
  ease: "easeInOut" as const,
  duration: 0.4,
};

// Page transition wrapper component
const PageTransition: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <motion.div
      initial="initial"
      animate="in"
      exit="out"
      variants={pageVariants}
      transition={pageTransition}
    >
      {children}
    </motion.div>
  );
};

// App wrapper with location-based transitions
const AppWithTransitions: React.FC = () => {
  const location = useLocation();
  
  // Development routes - only available in development
  const isDevelopment = process.env.NODE_ENV === 'development';

  return (
    <div className="app">
      <NavBar />
      <main className="view-port">
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route path="/" element={
              <PageTransition>
                <HeroPage />
              </PageTransition>
            } />
            <Route path="/movies" element={
              <PageTransition>
                <MovieView />
              </PageTransition>
            } />
            <Route path="/movie/:movieId" element={
              <PageTransition>
                <MovieDetails />
              </PageTransition>
            } />
            <Route path="/genres" element={
              <PageTransition>
                <GenresView />
              </PageTransition>
            } />
            <Route path="/genres/:genre" element={
              <PageTransition>
                <GenreMoviesView />
              </PageTransition>
            } />
            <Route path="/top-rated" element={
              <PageTransition>
                <MovieList filter={{ minRating: 8 }} />
              </PageTransition>
            } />
            <Route path="/recent" element={
              <PageTransition>
                <MovieList filter={{ minYear: 2020 }} />
              </PageTransition>
            } />
            <Route path="/about" element={
              <PageTransition>
                <About />
              </PageTransition>
            } />
            <Route path="/debug" element={
              <PageTransition>
                <Debug />
              </PageTransition>
            } />
            
            {/* Development-only routes */}
            {isDevelopment && (
              <>
                <Route path="/dev" element={
                  <PageTransition>
                    <DevelopmentRoutes />
                  </PageTransition>
                } />
                <Route path="/spinners-test" element={
                  <PageTransition>
                    <SpinnerTest />
                  </PageTransition>
                } />
              </>
            )}
          </Routes>
        </AnimatePresence>
      </main>
    </div>
  );
};
//             to="/movies"
//             className={`${HomeStyles.btnPrimary} btn-hover-lift`}
//           >
//             Browse Movies
//           </NavLink>
//           <NavLink
//             to="/top-rated"
//             className={`${HomeStyles.btnSecondary} btn-hover-lift`}
//           >
//             Top Rated
//           </NavLink>
//         </div>
//       </div>
//
//       <div className={HomeStyles.featuresGrid}>
//         <div className={`${HomeStyles.featureCard} card-hover`}>
//           <div className={HomeStyles.featureIcon}>🎭</div>
//           <h3>Extensive Collection</h3>
//           <p>Discover thousands of movies across all genres and decades</p>
//         </div>
//         <div className={`${HomeStyles.featureCard} card-hover`}>
//           <div className={HomeStyles.featureIcon}>⭐</div>
//           <h3>Curated Ratings</h3>
//           <p>IMDb and Rotten Tomatoes ratings to help you choose</p>
//         </div>
//         <div className={`${HomeStyles.featureCard} card-hover`}>
//           <div className={HomeStyles.featureIcon}>🔍</div>
//           <h3>Smart Search</h3>
//           <p>Find exactly what you're looking for with powerful filters</p>
//         </div>
//       </div>
//     </div>
//   );
// };


const About: React.FC = () => (
  <div>
    <h1>About</h1>
    <p>
      This is a FastAPI MongoDB Movies application built with React frontend.
    </p>
    <p>It demonstrates clean architecture with separation of concerns.</p>
  </div>
);

const Debug: React.FC = () => (
  <div>
    <ApiDebug />
  </div>
);



const App: React.FC = () => {
  return (
    <Router>
      <AppWithTransitions />
    </Router>
  );
};

export default App;
