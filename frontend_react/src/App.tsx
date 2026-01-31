import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import NavBar from './components/NavBar';
import MovieList from './components/MovieList';
import MovieDetails from './components/MovieDetails';
import ApiDebug from './components/ApiDebug';
import './App.css';

// Placeholder components for routes not yet implemented
const Home: React.FC = () => (
  <div className="content">
    <h1>Welcome to FastAPI Movies</h1>
    <p>Explore our collection of movies from the MongoDB sample_mflix dataset.</p>
    <p>Use the navigation above to browse movies by different categories.</p>
  </div>
);

const Users: React.FC = () => (
  <div className="content">
    <h1>Users</h1>
    <p>User management functionality coming soon...</p>
  </div>
);

const Comments: React.FC = () => (
  <div className="content">
    <h1>Comments</h1>
    <p>Comments section coming soon...</p>
  </div>
);

const Genres: React.FC = () => (
  <div className="content">
    <h1>Browse by Genre</h1>
    <MovieList />
  </div>
);

const Directors: React.FC = () => (
  <div className="content">
    <h1>Browse by Director</h1>
    <p>Director browsing coming soon...</p>
  </div>
);

const TopRated: React.FC = () => (
  <div className="content">
    <h1>Top Rated Movies</h1>
    <MovieList filter={{ minRating: 8 }} />
  </div>
);

const Recent: React.FC = () => (
  <div className="content">
    <h1>Recent Movies</h1>
    <MovieList filter={{ minYear: 2020 }} />
  </div>
);

const About: React.FC = () => (
  <div className="content">
    <h1>About</h1>
    <p>This is a FastAPI MongoDB Movies application built with React frontend.</p>
    <p>It demonstrates clean architecture with separation of concerns.</p>
  </div>
);

const Debug: React.FC = () => (
  <div className="content">
    <ApiDebug />
  </div>
);

const App: React.FC = () => {
  return (
    <Router>
      <div className="app">
        <NavBar />
        <div className="view-port">
          <div className="content">
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
          </div>
        </div>
      </div>
    </Router>
  );
};

export default App;