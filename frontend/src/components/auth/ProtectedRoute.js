import React from 'react';
import PropTypes from 'prop-types';

const ProtectedRoute = ({ children }) => {
  // In a real app, you would check authentication here
  const isAuthenticated = true; // Replace with actual auth check

  if (!isAuthenticated) {
    return (
      <div className="auth-required">
        <h2>Authentication Required</h2>
        <p>Please log in to access this page.</p>
      </div>
    );
  }

  return children;
};

ProtectedRoute.propTypes = {
  children: PropTypes.node.isRequired
};

export default ProtectedRoute;
