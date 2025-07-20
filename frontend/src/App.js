import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import ProtectedRoute from './components/auth/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import ModulesPage from './pages/ModulesPage';
import AIAssistantPage from './pages/AIAssistantPage';
import ProfilePage from './pages/ProfilePage';
import ErrorBoundary from './components/layout/ErrorBoundary';
import './App.css';

function App() {
  return (
    <div className="App">
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={
          <ErrorBoundary>
            <LoginPage />
          </ErrorBoundary>
        } />
        {/* Protected Routes */}
        <Route path="/" element={
          <ProtectedRoute>
            <Layout>
              <Navigate to="/dashboard" replace />
            </Layout>
          </ProtectedRoute>
        } />
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Layout>
              <ErrorBoundary>
                <DashboardPage />
              </ErrorBoundary>
            </Layout>
          </ProtectedRoute>
        } />
        <Route path="/modules" element={
          <ProtectedRoute>
            <Layout>
              <ErrorBoundary>
                <ModulesPage />
              </ErrorBoundary>
            </Layout>
          </ProtectedRoute>
        } />
        <Route path="/ai-tutor" element={
          <ProtectedRoute>
            <Layout>
              <ErrorBoundary>
                <AIAssistantPage />
              </ErrorBoundary>
            </Layout>
          </ProtectedRoute>
        } />
        <Route path="/profile" element={
          <ProtectedRoute>
            <Layout>
              <ErrorBoundary>
                <ProfilePage />
              </ErrorBoundary>
            </Layout>
          </ProtectedRoute>
        } />
        {/* Catch all route */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </div>
  );
}

export default App; 