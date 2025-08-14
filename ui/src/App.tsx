import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Outlet } from 'react-router-dom';
import HomePage from './pages/HomePage';
import TasksPage from './pages/TasksPage';
import CategoriesPage from './pages/CategoriesPage';
import WorkspacesPage from './pages/WorkspacesPage';
import ActivityPage from './pages/ActivityPage';
import LoginPage from './pages/LoginPage';
import { Header } from './components/Header';
import PrivateRoute from './components/PrivateRoute';
import './App.css';
import { websocketService } from './services/websocketService';
import { getToken } from './services/authService';

function App() {
  useEffect(() => {
    const token = getToken();
    if (token) {
      websocketService.connect(token);
    }
    return () => {
      websocketService.disconnect();
    };
  }, []);

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route element={<PrivateRoute />}>
            <Route element={
              <>
                <Header />
                <main className="container">
                  <Outlet />
                </main>
              </>
            }>
              <Route path="/" element={<HomePage />} />
              <Route path="/tasks" element={<TasksPage />} />
              <Route path="/categories" element={<CategoriesPage />} />
              <Route path="/workspaces" element={<WorkspacesPage />} />
              <Route path="/activity" element={<ActivityPage />} />
            </Route>
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;