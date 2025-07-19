import React, { useState, useEffect } from 'react';
import './ProfilePage.css';

const ProfilePage = () => {
  const [profile] = useState({
    username: 'CyberHacker',
    email: 'hacker@cipherquest.com',
    level: 5,
    xp: 2450,
    joinDate: '2024-01-15',
    bio: 'Passionate cybersecurity enthusiast learning ethical hacking and network security.',
    avatar: '👤'
  });

  const [achievements, setAchievements] = useState([]);
  const [stats, setStats] = useState({});
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    // Simulate loading profile data
    const loadProfileData = async () => {
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setAchievements([
        { id: 1, name: 'First Blood', description: 'Complete your first challenge', icon: '🩸', earned: true, date: '2024-01-20' },
        { id: 2, name: 'Code Breaker', description: 'Solve 10 cryptography challenges', icon: '🔓', earned: true, date: '2024-02-05' },
        { id: 3, name: 'Web Warrior', description: 'Complete web security module', icon: '🛡️', earned: true, date: '2024-02-15' },
        { id: 4, name: 'Network Ninja', description: 'Master network security concepts', icon: '🌐', earned: false, date: null },
        { id: 5, name: 'CTF Champion', description: 'Win a CTF competition', icon: '🏆', earned: false, date: null },
        { id: 6, name: 'Bug Hunter', description: 'Find and report 5 vulnerabilities', icon: '🐛', earned: false, date: null }
      ]);

      setStats({
        totalChallenges: 28,
        modulesCompleted: 12,
        currentStreak: 7,
        longestStreak: 15,
        totalTime: '45 hours',
        accuracy: 87,
        rank: 'Advanced'
      });
    };

    loadProfileData();
  }, []);

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'achievements', label: 'Achievements', icon: '🏆' },
    { id: 'stats', label: 'Statistics', icon: '📈' },
    { id: 'settings', label: 'Settings', icon: '⚙️' }
  ];

  const renderOverview = () => (
    <div className="overview-content">
      <div className="profile-card glass-effect">
        <div className="profile-header">
          <div className="profile-avatar">
            <span className="avatar-icon">{profile.avatar}</span>
          </div>
          <div className="profile-info">
            <h2 className="profile-name">{profile.username}</h2>
            <p className="profile-email">{profile.email}</p>
            <div className="profile-level">
              <span className="level-badge">Level {profile.level}</span>
              <span className="xp-info">{profile.xp} XP</span>
            </div>
          </div>
        </div>
        
        <div className="profile-bio">
          <p>{profile.bio}</p>
        </div>

        <div className="profile-meta">
          <div className="meta-item">
            <span className="meta-label">Member since</span>
            <span className="meta-value">{new Date(profile.joinDate).toLocaleDateString()}</span>
          </div>
          <div className="meta-item">
            <span className="meta-label">Rank</span>
            <span className="meta-value">{stats.rank}</span>
          </div>
        </div>
      </div>

      <div className="quick-stats">
        <div className="stat-item glass-effect">
          <div className="stat-icon">🎯</div>
          <div className="stat-content">
            <h3>{stats.totalChallenges}</h3>
            <p>Challenges Solved</p>
          </div>
        </div>
        <div className="stat-item glass-effect">
          <div className="stat-icon">📚</div>
          <div className="stat-content">
            <h3>{stats.modulesCompleted}</h3>
            <p>Modules Completed</p>
          </div>
        </div>
        <div className="stat-item glass-effect">
          <div className="stat-icon">🔥</div>
          <div className="stat-content">
            <h3>{stats.currentStreak}</h3>
            <p>Day Streak</p>
          </div>
        </div>
        <div className="stat-item glass-effect">
          <div className="stat-icon">⏱️</div>
          <div className="stat-content">
            <h3>{stats.totalTime}</h3>
            <p>Total Time</p>
          </div>
        </div>
      </div>
    </div>
  );

  const renderAchievements = () => (
    <div className="achievements-content">
      <div className="achievements-grid">
        {achievements.map((achievement) => (
          <div 
            key={achievement.id} 
            className={`achievement-card glass-effect ${achievement.earned ? 'earned' : 'locked'}`}
          >
            <div className="achievement-icon">
              {achievement.icon}
            </div>
            <div className="achievement-content">
              <h3 className="achievement-name">{achievement.name}</h3>
              <p className="achievement-description">{achievement.description}</p>
              {achievement.earned && (
                <div className="achievement-date">
                  Earned {new Date(achievement.date).toLocaleDateString()}
                </div>
              )}
            </div>
            <div className="achievement-status">
              {achievement.earned ? '✅' : '🔒'}
            </div>
          </div>
        ))}
      </div>
    </div>
  );

  const renderStats = () => (
    <div className="stats-content">
      <div className="stats-grid">
        <div className="stat-card glass-effect">
          <h3>Performance Overview</h3>
          <div className="performance-stats">
            <div className="performance-item">
              <span className="performance-label">Accuracy</span>
              <div className="performance-bar">
                <div 
                  className="performance-fill"
                  style={{ width: `${stats.accuracy}%` }}
                />
              </div>
              <span className="performance-value">{stats.accuracy}%</span>
            </div>
            <div className="performance-item">
              <span className="performance-label">Streak</span>
              <div className="performance-bar">
                <div 
                  className="performance-fill"
                  style={{ width: `${(stats.currentStreak / stats.longestStreak) * 100}%` }}
                />
              </div>
              <span className="performance-value">{stats.currentStreak} days</span>
            </div>
          </div>
        </div>

        <div className="stat-card glass-effect">
          <h3>Learning Progress</h3>
          <div className="progress-chart">
            <div className="chart-item">
              <span className="chart-label">Cryptography</span>
              <div className="chart-bar">
                <div className="chart-fill" style={{ width: '85%' }}></div>
              </div>
              <span className="chart-value">85%</span>
            </div>
            <div className="chart-item">
              <span className="chart-label">Web Security</span>
              <div className="chart-bar">
                <div className="chart-fill" style={{ width: '60%' }}></div>
              </div>
              <span className="chart-value">60%</span>
            </div>
            <div className="chart-item">
              <span className="chart-label">Network Security</span>
              <div className="chart-bar">
                <div className="chart-fill" style={{ width: '40%' }}></div>
              </div>
              <span className="chart-value">40%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderSettings = () => (
    <div className="settings-content">
      <div className="settings-section glass-effect">
        <h3>Account Settings</h3>
        <div className="setting-item">
          <label htmlFor="username" className="setting-label">Username</label>
          <input 
            id="username"
            type="text" 
            value={profile.username} 
            className="setting-input"
            readOnly
          />
        </div>
        <div className="setting-item">
          <label htmlFor="email" className="setting-label">Email</label>
          <input 
            id="email"
            type="email" 
            value={profile.email} 
            className="setting-input"
            readOnly
          />
        </div>
        <div className="setting-item">
          <label htmlFor="bio" className="setting-label">Bio</label>
          <textarea 
            id="bio"
            value={profile.bio} 
            className="setting-textarea"
            rows="3"
            readOnly
          />
        </div>
      </div>

      <div className="settings-section glass-effect">
        <h3>Preferences</h3>
        <div className="setting-item">
          <label htmlFor="theme" className="setting-label">Theme</label>
          <select id="theme" className="setting-select" defaultValue="dark">
            <option value="dark">Dark Theme</option>
            <option value="light">Light Theme</option>
            <option value="auto">Auto</option>
          </select>
        </div>
        <div className="setting-item">
          <label className="setting-label">Notifications</label>
          <div className="setting-toggle">
            <input type="checkbox" id="notifications" defaultChecked />
            <label htmlFor="notifications">Enable notifications</label>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="profile-page">
      {/* Header */}
      <div className="profile-header-section">
        <h1 className="page-title">Profile</h1>
        <p className="page-subtitle">Manage your account and view your progress</p>
      </div>

      {/* Tab Navigation */}
      <div className="tab-navigation glass-effect">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <span className="tab-icon">{tab.icon}</span>
            <span className="tab-label">{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'overview' && renderOverview()}
        {activeTab === 'achievements' && renderAchievements()}
        {activeTab === 'stats' && renderStats()}
        {activeTab === 'settings' && renderSettings()}
      </div>
    </div>
  );
};

export default ProfilePage;
