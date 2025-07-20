import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import '../styles/LoginPage.css';

const LoginPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (!isLogin && formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) {
      return;
    }
    setLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      localStorage.setItem('authToken', 'dummy-token');
      const from = location.state?.from?.pathname || '/dashboard';
      navigate(from, { replace: true });
    } catch (error) {
      console.error('Authentication error:', error);
      setErrors({ general: 'Authentication failed. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    setFormData({ email: '', password: '', confirmPassword: '' });
    setErrors({});
  };

  return (
    <div className="login-page" role="main" aria-label="Login Page">
      <div className="login-container glass-effect">
        <div className="login-header">
          <h1 className="login-title">
            <span className="text-gradient">Cipher</span>Quest
          </h1>
          <p className="login-subtitle">
            {isLogin ? 'Welcome back, hacker!' : 'Join the cyber revolution!'}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="login-form" aria-label="Login form">
          {errors.general && (
            <div className="error-message" role="alert">
              {errors.general}
            </div>
          )}

          <div className="form-group">
            <label htmlFor="email" className="form-label">Email</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              className={`form-input ${errors.email ? 'error' : ''}`}
              placeholder="Enter your email"
              aria-required="true"
              aria-invalid={!!errors.email}
              autoComplete="username"
            />
            {errors.email && <span className="error-text" role="alert">{errors.email}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="password" className="form-label">Password</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              className={`form-input ${errors.password ? 'error' : ''}`}
              placeholder="Enter your password"
              aria-required="true"
              aria-invalid={!!errors.password}
              autoComplete={isLogin ? "current-password" : "new-password"}
            />
            {errors.password && <span className="error-text" role="alert">{errors.password}</span>}
          </div>

          {!isLogin && (
            <div className="form-group">
              <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
              <input
                type="password"
                id="confirmPassword"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleInputChange}
                className={`form-input ${errors.confirmPassword ? 'error' : ''}`}
                placeholder="Confirm your password"
                aria-required="true"
                aria-invalid={!!errors.confirmPassword}
                autoComplete="new-password"
              />
              {errors.confirmPassword && <span className="error-text" role="alert">{errors.confirmPassword}</span>}
            </div>
          )}

          <button type="submit" className="submit-btn" disabled={loading} aria-busy={loading} aria-label={isLogin ? 'Login' : 'Sign Up'}>
            {loading ? <span className="loading-spinner" aria-hidden="true"></span> : (isLogin ? 'Login' : 'Sign Up')}
          </button>
        </form>

        <div className="login-footer">
          <button onClick={toggleMode} className="toggle-mode-btn" tabIndex={0} aria-label={isLogin ? 'Switch to sign up' : 'Switch to login'}>
            {isLogin ? "Don't have an account? Sign up" : 'Already have an account? Login'}
          </button>
        </div>

        <div className="social-login">
          <p className="social-login-text">Or continue with</p>
          <div className="social-buttons">
            <button className="social-btn google-btn" tabIndex={0} aria-label="Continue with Google">
              <span className="social-icon">🔍</span>
              {' '}Google
            </button>
            <button className="social-btn github-btn" tabIndex={0} aria-label="Continue with GitHub">
              <span className="social-icon">🐙</span>
              {' '}GitHub
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
