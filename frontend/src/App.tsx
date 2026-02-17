import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
} from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import NavBar from "./components/ui/nav/NavBar";
import MovieDetails from "./components/movies/MovieDetails";
import GenreMoviesView from "./components/genres/GenreMoviesView";
import ApiDebug from "./components/util/ApiDebug";
import MoviePage from "./components/pages/MoviePage";
import HomePage from "./components/pages/HomePage";
import DevelopmentRoutes from "./components/dev/DevelopmentRoutes";
import SpinnerTest from "./components/dev/SpinnerTest";
import GenresPage from "./components/pages/GenresPage";
import AboutPage from "./components/pages/AboutPage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

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
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <NavBar />
      <main id="main-content" className="view-port">
        <AnimatePresence mode="wait">
          <Routes location={location} key={location.pathname}>
            <Route path="/" element={
              <PageTransition>
                <HomePage />
              </PageTransition>
            } />
            <Route path="/movies" element={
              <PageTransition>
                <MoviePage />
              </PageTransition>
            } />
            <Route path="/movie/:movieId" element={
              <PageTransition>
                <MovieDetails />
              </PageTransition>
            } />
            <Route path="/genres" element={
              <PageTransition>
                <GenresPage />
              </PageTransition>
            } />
            <Route path="/genres/:genre" element={
              <PageTransition>
                <GenreMoviesView />
              </PageTransition>
            } />
            <Route path="/top-rated" element={
              <PageTransition>
                <MoviePage filter={{ minRating: 8 }} />
              </PageTransition>
            } />
            <Route path="/recent" element={
              <PageTransition>
                <MoviePage filter={{ minYear: 2000 }} />
              </PageTransition>
            } />
            <Route path="/about" element={
              <PageTransition>
                <AboutPage />
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




const Debug: React.FC = () => (
  <div>
    <ApiDebug />
  </div>
);



const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <AppWithTransitions />
      </Router>
    </QueryClientProvider>
  );
};

export default App;
