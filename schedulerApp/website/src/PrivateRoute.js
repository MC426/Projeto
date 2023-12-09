import React from 'react';
import { Route, Navigate } from 'react-router-dom';
import { useUser } from './UserProvider';

const PrivateRoute = ({ children }) => {
  const { userData, } = useUser();
  return userData ? children : <Navigate to="/login" />;
};

export default PrivateRoute;