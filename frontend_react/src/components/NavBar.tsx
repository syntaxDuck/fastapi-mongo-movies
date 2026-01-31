import React from 'react';
import { NavLink } from 'react-router-dom';
import './NavBar.css';

const NavBar: React.FC = () => {
  return (
    <nav className="nav-bar">
      <ul className="nav-list">
        <li>
          <NavLink to="/" className={({ isActive }) => isActive ? 'active' : ''}>
            Home
          </NavLink>
        </li>
        <li>
          <NavLink to="/movies" className={({ isActive }) => isActive ? 'active' : ''}>
            Movies
          </NavLink>
        </li>
        <li>
          <NavLink to="/users" className={({ isActive }) => isActive ? 'active' : ''}>
            Users
          </NavLink>
        </li>
        <li>
          <NavLink to="/comments" className={({ isActive }) => isActive ? 'active' : ''}>
            Comments
          </NavLink>
        </li>
        <li>
          <NavLink to="/genres" className={({ isActive }) => isActive ? 'active' : ''}>
            Genres
          </NavLink>
        </li>
        <li>
          <NavLink to="/directors" className={({ isActive }) => isActive ? 'active' : ''}>
            Directors
          </NavLink>
        </li>
        <li>
          <NavLink to="/top-rated" className={({ isActive }) => isActive ? 'active' : ''}>
            Top Rated
          </NavLink>
        </li>
        <li>
          <NavLink to="/recent" className={({ isActive }) => isActive ? 'active' : ''}>
            Recent
          </NavLink>
        </li>
        <li>
          <NavLink to="/about" className={({ isActive }) => isActive ? 'active' : ''}>
            About
          </NavLink>
        </li>
        <li>
          <NavLink to="/debug" className={({ isActive }) => isActive ? 'active' : ''}>
            Debug
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default NavBar;