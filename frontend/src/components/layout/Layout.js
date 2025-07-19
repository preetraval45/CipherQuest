import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import PropTypes from 'prop-types';
import './Layout.css';

const Layout = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', icon: '📊' },
    { path: '/modules', label: 'Modules', icon: '📚' },
    { path: '/ai-tutor', label: 'AI Tutor', icon: '🤖' },
    { path: '/profile', label: 'Profile', icon: '👤' }
  ];

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const handleOverlayClick = () => {
    setSidebarOpen(false);
  };

  const handleOverlayKeyDown = (e) => {
    if (e.key === 'Escape') {
      setSidebarOpen(false);
    }
  };

  return (
    <div className="layout">
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h2 className="logo">
            <span className="text-gradient">Cipher</span>Quest
          </h2>
          <button className="close-btn" onClick={toggleSidebar}>
            ✕
          </button>
        </div>
        
        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
              onClick={() => setSidebarOpen(false)}
            >
              <span className="nav-icon">{item.icon}</span>
              <span className="nav-label">{item.label}</span>
            </Link>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="user-info">
            <div className="user-avatar">👤</div>
            <div className="user-details">
              <div className="user-name">Hacker</div>
              <div className="user-rank">Level 5</div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {/* Top Bar */}
        <header className="top-bar">
          <button className="menu-btn" onClick={toggleSidebar}>
            ☰
          </button>
          
          <div className="top-bar-center">
            <h1 className="page-title">
              {navItems.find(item => item.path === location.pathname)?.label || 'CipherQuest'}
            </h1>
          </div>

          <div className="top-bar-right">
            <div className="notifications">
              <span className="notification-icon">🔔</span>
              <span className="notification-badge">3</span>
            </div>
            <div className="user-menu">
              <span className="user-menu-icon">👤</span>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="page-content">
          {children}
        </div>
      </main>

      {/* Mobile Overlay */}
      {sidebarOpen && (
        <button 
          className="mobile-overlay" 
          onClick={handleOverlayClick}
          onKeyDown={handleOverlayKeyDown}
          aria-label="Close sidebar"
        />
      )}
    </div>
  );
};

Layout.propTypes = {
  children: PropTypes.node.isRequired
};

export default Layout;
