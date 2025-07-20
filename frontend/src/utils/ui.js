// UI utility functions

/**
 * Get activity icon based on activity type
 * @param {string} type - Activity type
 * @returns {string} Emoji icon
 */
export const getActivityIcon = (type) => {
  switch (type) {
    case 'module': return '📚';
    case 'challenge': return '🎯';
    case 'achievement': return '🏆';
    case 'quiz': return '❓';
    case 'badge': return '🏅';
    default: return '📝';
  }
};

/**
 * Get status color for activity status
 * @param {string} status - Activity status
 * @returns {string} CSS color value
 */
export const getStatusColor = (status) => {
  switch (status) {
    case 'completed': return 'var(--success-color)';
    case 'started': return 'var(--warning-color)';
    case 'earned': return 'var(--primary-color)';
    case 'failed': return 'var(--error-color)';
    case 'in_progress': return 'var(--info-color)';
    default: return 'var(--text-secondary)';
  }
};

/**
 * Get difficulty color for challenges/modules
 * @param {string} difficulty - Difficulty level
 * @returns {string} CSS color value
 */
export const getDifficultyColor = (difficulty) => {
  switch (difficulty?.toLowerCase()) {
    case 'easy': return 'var(--success-color)';
    case 'medium': return 'var(--warning-color)';
    case 'hard': return 'var(--error-color)';
    case 'expert': return 'var(--primary-color)';
    default: return 'var(--text-secondary)';
  }
};

/**
 * Format number with locale-specific formatting
 * @param {number} number - Number to format
 * @returns {string} Formatted number
 */
export const formatNumber = (number) => {
  return number.toLocaleString();
};

/**
 * Format XP with appropriate suffix
 * @param {number} xp - XP value
 * @returns {string} Formatted XP
 */
export const formatXP = (xp) => {
  if (xp >= 1000000) {
    return `${(xp / 1000000).toFixed(1)}M XP`;
  }
  if (xp >= 1000) {
    return `${(xp / 1000).toFixed(1)}K XP`;
  }
  return `${xp} XP`;
};

/**
 * Get rank badge emoji
 * @param {number} rank - Player rank
 * @returns {string} Rank badge emoji
 */
export const getRankBadge = (rank) => {
  switch (rank) {
    case 1: return '🥇';
    case 2: return '🥈';
    case 3: return '🥉';
    default: return `#${rank}`;
  }
};

/**
 * Generate random loading delay for better UX
 * @param {number} min - Minimum delay in ms
 * @param {number} max - Maximum delay in ms
 * @returns {Promise} Promise that resolves after random delay
 */
export const randomDelay = (min = 500, max = 2000) => {
  const delay = Math.random() * (max - min) + min;
  return new Promise(resolve => setTimeout(resolve, delay));
};

/**
 * Debounce function to limit API calls
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in ms
 * @returns {Function} Debounced function
 */
export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}; 