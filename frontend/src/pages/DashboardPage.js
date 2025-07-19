import React, { useState, useEffect } from 'react';
import './DashboardPage.css';

const DashboardPage = () => {
  const [stats, setStats] = useState({
    xp: 0,
    level: 1,
    modulesCompleted: 0,
    challengesSolved: 0,
    streak: 0
  });

  const [recentActivity, setRecentActivity] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    // Simulate loading data
    const loadDashboardData = async () => {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setStats({
        xp: 2450,
        level: 5,
        modulesCompleted: 12,
        challengesSolved: 28,
        streak: 7
      });

      setRecentActivity([
        { id: 1, type: 'module', title: 'Cryptography Basics', time: '2 hours ago', status: 'completed' },
        { id: 2, type: 'challenge', title: 'Caesar Cipher', time: '1 day ago', status: 'completed' },
        { id: 3, type: 'achievement', title: 'First Blood', time: '2 days ago', status: 'earned' },
        { id: 4, type: 'module', title: 'Network Security', time: '3 days ago', status: 'started' }
      ]);

      setLeaderboard([
        { rank: 1, name: 'CyberNinja', xp: 15420, level: 12 },
        { rank: 2, name: 'HackMaster', xp: 12850, level: 11 },
        { rank: 3, name: 'CodeBreaker', xp: 11230, level: 10 },
        { rank: 4, name: 'SecurityPro', xp: 9870, level: 9 },
        { rank: 5, name: 'CipherLord', xp: 8540, level: 8 }
      ]);
    };

    loadDashboardData();
  }, []);

  const getActivityIcon = (type) => {
    switch (type) {
      case 'module': return '📚';
      case 'challenge': return '🎯';
      case 'achievement': return '🏆';
      default: return '📝';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'var(--success-color)';
      case 'started': return 'var(--warning-color)';
      case 'earned': return 'var(--primary-color)';
      default: return 'var(--text-secondary)';
    }
  };

  return (
    <div className="dashboard-page">
      {/* Welcome Section */}
      <div className="welcome-section glass-effect">
        <div className="welcome-content">
          <h2 className="welcome-title">
            Welcome back, <span className="text-gradient">Hacker</span>! 🚀
          </h2>
          <p className="welcome-subtitle">
            Ready to continue your cybersecurity journey?
          </p>
        </div>
        <div className="welcome-avatar">
          <div className="avatar-circle">
            <span className="avatar-icon">👤</span>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="stats-grid">
        <div className="stat-card glass-effect">
          <div className="stat-icon">⭐</div>
          <div className="stat-content">
            <h3 className="stat-value">{stats.xp.toLocaleString()}</h3>
            <p className="stat-label">Total XP</p>
          </div>
        </div>

        <div className="stat-card glass-effect">
          <div className="stat-icon">📊</div>
          <div className="stat-content">
            <h3 className="stat-value">Level {stats.level}</h3>
            <p className="stat-label">Current Level</p>
          </div>
        </div>

        <div className="stat-card glass-effect">
          <div className="stat-icon">📚</div>
          <div className="stat-content">
            <h3 className="stat-value">{stats.modulesCompleted}</h3>
            <p className="stat-label">Modules Completed</p>
          </div>
        </div>

        <div className="stat-card glass-effect">
          <div className="stat-icon">🎯</div>
          <div className="stat-content">
            <h3 className="stat-value">{stats.challengesSolved}</h3>
            <p className="stat-label">Challenges Solved</p>
          </div>
        </div>

        <div className="stat-card glass-effect">
          <div className="stat-icon">🔥</div>
          <div className="stat-content">
            <h3 className="stat-value">{stats.streak}</h3>
            <p className="stat-label">Day Streak</p>
          </div>
        </div>
      </div>

      {/* Main Content Grid */}
      <div className="dashboard-grid">
        {/* Recent Activity */}
        <div className="activity-section glass-effect">
          <div className="section-header">
            <h3 className="section-title">Recent Activity</h3>
            <button className="view-all-btn">View All</button>
          </div>
          
          <div className="activity-list">
            {recentActivity.map((activity) => (
              <div key={activity.id} className="activity-item">
                <div className="activity-icon">
                  {getActivityIcon(activity.type)}
                </div>
                <div className="activity-content">
                  <h4 className="activity-title">{activity.title}</h4>
                  <p className="activity-time">{activity.time}</p>
                </div>
                <div 
                  className="activity-status"
                  style={{ color: getStatusColor(activity.status) }}
                >
                  {activity.status}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Leaderboard */}
        <div className="leaderboard-section glass-effect">
          <div className="section-header">
            <h3 className="section-title">Top Hackers</h3>
            <button className="view-all-btn">View All</button>
          </div>
          
          <div className="leaderboard-list">
            {leaderboard.map((player) => (
              <div key={player.rank} className="leaderboard-item">
                <div className="rank-badge">
                  {player.rank === 1 && '🥇'}
                  {player.rank === 2 && '🥈'}
                  {player.rank === 3 && '🥉'}
                  {player.rank > 3 && `#${player.rank}`}
                </div>
                <div className="player-info">
                  <h4 className="player-name">{player.name}</h4>
                  <p className="player-level">Level {player.level}</p>
                </div>
                <div className="player-xp">
                  {player.xp.toLocaleString()} XP
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recommended Challenges */}
        <div className="recommended-section glass-effect">
          <div className="section-header">
            <h3 className="section-title">Recommended for You</h3>
          </div>
          
          <div className="recommended-list">
            <div className="recommended-item">
              <div className="recommended-icon">🔐</div>
              <div className="recommended-content">
                <h4 className="recommended-title">Advanced Encryption</h4>
                <p className="recommended-desc">Master modern encryption techniques</p>
                <div className="recommended-meta">
                  <span className="difficulty easy">Easy</span>
                  <span className="duration">30 min</span>
                </div>
              </div>
            </div>

            <div className="recommended-item">
              <div className="recommended-icon">🌐</div>
              <div className="recommended-content">
                <h4 className="recommended-title">Web Security</h4>
                <p className="recommended-desc">Learn about web vulnerabilities</p>
                <div className="recommended-meta">
                  <span className="difficulty medium">Medium</span>
                  <span className="duration">45 min</span>
                </div>
              </div>
            </div>

            <div className="recommended-item">
              <div className="recommended-icon">🛡️</div>
              <div className="recommended-content">
                <h4 className="recommended-title">Penetration Testing</h4>
                <p className="recommended-desc">Ethical hacking fundamentals</p>
                <div className="recommended-meta">
                  <span className="difficulty hard">Hard</span>
                  <span className="duration">60 min</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
