import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  NavLink,
} from "react-router-dom";
import NavBar from "./components/NavBar";
import MovieList from "./components/MovieList";
import GenreList from "./components/GenreList";
import MovieDetails from "./components/MovieDetails";
import ApiDebug from "./components/ApiDebug";

// Import consolidated stylesheet
import "./styles/index.css";

// Placeholder components for routes not yet implemented
import HomeStyles from "./styles/pages/Home.module.css";

const Home: React.FC = () => {
  return (
    <div className="fade-in">
      <div className={HomeStyles.heroSection}>
        <h1 className={HomeStyles.heroTitle}>🎬 Welcome to MovieDB</h1>
        <p className={HomeStyles.heroSubtitle}>
          Explore our curated collection of movies from the MongoDB sample_mflix
          dataset
        </p>
        <div className={HomeStyles.heroActions}>
          <NavLink
            to="/movies"
            className={`${HomeStyles.btnPrimary} btn-hover-lift`}
          >
            Browse Movies
          </NavLink>
          <NavLink
            to="/top-rated"
            className={`${HomeStyles.btnSecondary} btn-hover-lift`}
          >
            Top Rated
          </NavLink>
        </div>
      </div>

      <div className={HomeStyles.featuresGrid}>
        <div className={`${HomeStyles.featureCard} card-hover`}>
          <div className={HomeStyles.featureIcon}>🎭</div>
          <h3>Extensive Collection</h3>
          <p>Discover thousands of movies across all genres and decades</p>
        </div>
        <div className={`${HomeStyles.featureCard} card-hover`}>
          <div className={HomeStyles.featureIcon}>⭐</div>
          <h3>Curated Ratings</h3>
          <p>IMDb and Rotten Tomatoes ratings to help you choose</p>
        </div>
        <div className={`${HomeStyles.featureCard} card-hover`}>
          <div className={HomeStyles.featureIcon}>🔍</div>
          <h3>Smart Search</h3>
          <p>Find exactly what you're looking for with powerful filters</p>
        </div>
      </div>
    </div>
  );
};

const Users: React.FC = () => (
  <div>
    <h1>Users</h1>
    <p>User management functionality coming soon...</p>
  </div>
);

const Comments: React.FC = () => (
  <div>
    <h1>Comments</h1>
    <p>Comments section coming soon...</p>
  </div>
);

const Genres: React.FC = () => (
  <div>
    <h1>Browse by Genre</h1>
    <GenreList />
  </div>
);

const Directors: React.FC = () => (
  <div>
    <h1>Browse by Director</h1>
    <p>Director browsing coming soon...</p>
  </div>
);

const TopRated: React.FC = () => (
  <div>
    <h1>Top Rated Movies</h1>
    <MovieList filter={{ minRating: 8 }} />
  </div>
);

const Recent: React.FC = () => (
  <div>
    <h1>Recent Movies</h1>
    <MovieList filter={{ minYear: 2020 }} />
  </div>
);

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
      <div className="app">
        <NavBar />
        <div className="view-port">
          <main className="content">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/movies" element={<MovieList />} />
              <Route path="/movie/:movieId" element={<MovieDetails />} />
              <Route path="/users" element={<Users />} />
              <Route path="/comments" element={<Comments />} />
              <Route path="/genres" element={<Genres />} />
              <Route path="/directors" element={<Directors />} />
              <Route path="/top-rated" element={<TopRated />} />
              <Route path="/recent" element={<Recent />} />
              <Route path="/about" element={<About />} />
              <Route path="/debug" element={<Debug />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
};

export default App;
