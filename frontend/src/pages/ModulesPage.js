import React, { useState, useEffect } from 'react';
import './ModulesPage.css';

const ModulesPage = () => {
  const [modules, setModules] = useState([]);
  const [filteredModules, setFilteredModules] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  const [viewMode, setViewMode] = useState('grid'); // 'grid' or 'list'

  useEffect(() => {
    // Simulate loading modules data
    const loadModules = async () => {
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const modulesData = [
        {
          id: 1,
          title: 'Cryptography Basics',
          description: 'Learn the fundamentals of encryption and decryption techniques',
          difficulty: 'beginner',
          duration: '2 hours',
          lessons: 8,
          progress: 100,
          category: 'Cryptography',
          icon: '🔐',
          tags: ['encryption', 'decryption', 'ciphers']
        },
        {
          id: 2,
          title: 'Network Security',
          description: 'Understand network vulnerabilities and protection methods',
          difficulty: 'intermediate',
          duration: '3 hours',
          lessons: 12,
          progress: 60,
          category: 'Networking',
          icon: '🌐',
          tags: ['networking', 'firewalls', 'protocols']
        },
        {
          id: 3,
          title: 'Web Application Security',
          description: 'Master web security vulnerabilities and countermeasures',
          difficulty: 'advanced',
          duration: '4 hours',
          lessons: 15,
          progress: 0,
          category: 'Web Security',
          icon: '🛡️',
          tags: ['web', 'vulnerabilities', 'OWASP']
        },
        {
          id: 4,
          title: 'Penetration Testing',
          description: 'Learn ethical hacking and security assessment techniques',
          difficulty: 'advanced',
          duration: '5 hours',
          lessons: 18,
          progress: 0,
          category: 'Ethical Hacking',
          icon: '🎯',
          tags: ['pentesting', 'ethical hacking', 'assessment']
        },
        {
          id: 5,
          title: 'Malware Analysis',
          description: 'Analyze and understand malicious software behavior',
          difficulty: 'intermediate',
          duration: '3.5 hours',
          lessons: 14,
          progress: 0,
          category: 'Malware',
          icon: '🦠',
          tags: ['malware', 'analysis', 'reverse engineering']
        },
        {
          id: 6,
          title: 'Social Engineering',
          description: 'Understand human psychology in cybersecurity',
          difficulty: 'beginner',
          duration: '2.5 hours',
          lessons: 10,
          progress: 0,
          category: 'Social Engineering',
          icon: '🧠',
          tags: ['psychology', 'social engineering', 'phishing']
        }
      ];
      
      setModules(modulesData);
      setFilteredModules(modulesData);
    };

    loadModules();
  }, []);

  useEffect(() => {
    // Filter modules based on search term and difficulty
    let filtered = modules;

    if (searchTerm) {
      filtered = filtered.filter(module =>
        module.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        module.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        module.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    if (selectedDifficulty !== 'all') {
      filtered = filtered.filter(module => module.difficulty === selectedDifficulty);
    }

    setFilteredModules(filtered);
  }, [searchTerm, selectedDifficulty, modules]);

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'beginner': return 'var(--success-color)';
      case 'intermediate': return 'var(--warning-color)';
      case 'advanced': return 'var(--error-color)';
      default: return 'var(--text-secondary)';
    }
  };

  const getProgressColor = (progress) => {
    if (progress === 100) return 'var(--success-color)';
    if (progress > 50) return 'var(--warning-color)';
    return 'var(--primary-color)';
  };

  return (
    <div className="modules-page">
      {/* Header */}
      <div className="modules-header">
        <div className="header-content">
          <h1 className="page-title">Learning Modules</h1>
          <p className="page-subtitle">Master cybersecurity concepts through interactive modules</p>
        </div>
      </div>

      {/* Filters and Search */}
      <div className="modules-controls glass-effect">
        <div className="search-section">
          <div className="search-input-wrapper">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="Search modules..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>
        </div>

        <div className="filters-section">
          <div className="difficulty-filter">
            <label htmlFor="difficulty-select" className="filter-label">Difficulty:</label>
            <select
              id="difficulty-select"
              value={selectedDifficulty}
              onChange={(e) => setSelectedDifficulty(e.target.value)}
              className="filter-select"
            >
              <option value="all">All Levels</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div className="view-toggle">
            <button
              className={`view-btn ${viewMode === 'grid' ? 'active' : ''}`}
              onClick={() => setViewMode('grid')}
            >
              📱
            </button>
            <button
              className={`view-btn ${viewMode === 'list' ? 'active' : ''}`}
              onClick={() => setViewMode('list')}
            >
              📋
            </button>
          </div>
        </div>
      </div>

      {/* Results Count */}
      <div className="results-info">
        <p>Showing {filteredModules.length} of {modules.length} modules</p>
      </div>

      {/* Modules Grid/List */}
      <div className={`modules-container ${viewMode}`}>
        {filteredModules.map((module) => (
          <div key={module.id} className="module-card glass-effect">
            <div className="module-header">
              <div className="module-icon">
                {module.icon}
              </div>
              <div className="module-meta">
                <span 
                  className="difficulty-badge"
                  style={{ color: getDifficultyColor(module.difficulty) }}
                >
                  {module.difficulty}
                </span>
                <span className="category-badge">{module.category}</span>
              </div>
            </div>

            <div className="module-content">
              <h3 className="module-title">{module.title}</h3>
              <p className="module-description">{module.description}</p>
              
              <div className="module-stats">
                <div className="stat">
                  <span className="stat-icon">⏱️</span>
                  <span className="stat-text">{module.duration}</span>
                </div>
                <div className="stat">
                  <span className="stat-icon">📚</span>
                  <span className="stat-text">{module.lessons} lessons</span>
                </div>
              </div>

              <div className="module-progress">
                <div className="progress-header">
                  <span className="progress-label">Progress</span>
                  <span className="progress-percentage">{module.progress}%</span>
                </div>
                <div className="progress-bar">
                  <div 
                    className="progress-fill"
                    style={{ 
                      width: `${module.progress}%`,
                      backgroundColor: getProgressColor(module.progress)
                    }}
                  />
                </div>
              </div>

              <div className="module-tags">
                {module.tags.slice(0, 3).map((tag) => (
                  <span key={`tag-${tag}`} className="tag">{tag}</span>
                ))}
              </div>
            </div>

            <div className="module-actions">
              {module.progress === 100 ? (
                <button className="action-btn completed">
                  <span>✅ Completed</span>
                </button>
              ) : module.progress > 0 ? (
                <button className="action-btn continue">
                  <span>▶️ Continue</span>
                </button>
              ) : (
                <button className="action-btn start">
                  <span>🚀 Start Module</span>
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {filteredModules.length === 0 && (
        <div className="empty-state glass-effect">
          <div className="empty-icon">🔍</div>
          <h3>No modules found</h3>
          <p>Try adjusting your search terms or filters</p>
          <button 
            className="reset-filters-btn"
            onClick={() => {
              setSearchTerm('');
              setSelectedDifficulty('all');
            }}
          >
            Reset Filters
          </button>
        </div>
      )}
    </div>
  );
};

export default ModulesPage;
