import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="home-content">
      <h1>Welcome to Todo Manager</h1>
      <div className="cta-buttons">
        <ul>
          <li>
            <Link to="/tasks" className="cta-button">
              View Tasks
            </Link>
          </li>
          <li>
            <Link to="/categories" className="cta-button">
              Manage Categories
            </Link>
          </li>
        </ul>
      </div>
    </div>
  );
};

export default HomePage;