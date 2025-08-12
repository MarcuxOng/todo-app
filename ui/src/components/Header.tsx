import { Link } from 'react-router-dom';
import './Navbar.css';
import * as authService from '../services/authService';

export const Header = () => {
  const handleLogout = async () => {
    try {
      await authService.logout();
      window.location.href = '/login';
    } catch (error) {
      console.error('Logout failed:', error);
      alert('Failed to logout. Please try again.');
    }
  };

  return (
    <nav className="navbar">
      <div className="nav-container">
        {/* <h1 className="nav-brand">TodoApp</h1> */}
        <Link to="/" className="nav-brand">TodoApp</Link>
        <ul className="nav-menu">
          {/* <li className="nav-item">
            <Link to="/" className="nav-link">Home</Link>
          </li> */}
          <li className="nav-item">
            <Link to="/tasks" className="nav-link">Tasks</Link>
          </li>
          <li className="nav-item">
            <Link to="/categories" className="nav-link">Categories</Link>
          </li>
          <li className="nav-item">
            <button
              onClick={handleLogout}
              className="nav-link logout-btn"
            >
              Logout
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
};