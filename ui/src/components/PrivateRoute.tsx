import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import * as authService from '../services/authService';

const PrivateRoute: React.FC = () => {
  const isAuthenticated = authService.getToken();

  return isAuthenticated ? <Outlet /> : <Navigate to="/login" />;
};

export default PrivateRoute;