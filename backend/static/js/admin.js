// CipherQuest Backend Admin JavaScript

/**
 * Admin dashboard functionality
 */
class AdminDashboard {
  constructor() {
    this.init();
  }

  init() {
    this.bindEvents();
    this.loadStats();
  }

  bindEvents() {
    // Bind admin panel events
    document.addEventListener('DOMContentLoaded', () => {
      this.setupEventListeners();
    });
  }

  setupEventListeners() {
    // User management
    const userTable = document.getElementById('user-table');
    if (userTable) {
      userTable.addEventListener('click', (e) => {
        if (e.target.classList.contains('ban-user')) {
          this.banUser(e.target.dataset.userId);
        }
        if (e.target.classList.contains('delete-user')) {
          this.deleteUser(e.target.dataset.userId);
        }
      });
    }

    // Module management
    const moduleForm = document.getElementById('module-form');
    if (moduleForm) {
      moduleForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.createModule(new FormData(moduleForm));
      });
    }

    // Challenge management
    const challengeForm = document.getElementById('challenge-form');
    if (challengeForm) {
      challengeForm.addEventListener('submit', (e) => {
        e.preventDefault();
        this.createChallenge(new FormData(challengeForm));
      });
    }
  }

  async loadStats() {
    try {
      const response = await fetch('/api/admin/stats');
      const stats = await response.json();
      this.updateStatsDisplay(stats);
    } catch (error) {
      console.error('Failed to load admin stats:', error);
    }
  }

  updateStatsDisplay(stats) {
    const statsContainer = document.getElementById('admin-stats');
    if (!statsContainer) return;

    statsContainer.innerHTML = `
      <div class="stat-card">
        <h3>Total Users</h3>
        <p>${stats.total_users}</p>
      </div>
      <div class="stat-card">
        <h3>Active Users</h3>
        <p>${stats.active_users}</p>
      </div>
      <div class="stat-card">
        <h3>Total Modules</h3>
        <p>${stats.total_modules}</p>
      </div>
      <div class="stat-card">
        <h3>Total Challenges</h3>
        <p>${stats.total_challenges}</p>
      </div>
    `;
  }

  async banUser(userId) {
    if (!confirm('Are you sure you want to ban this user?')) return;

    try {
      const response = await fetch(`/api/admin/users/${userId}/ban`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (response.ok) {
        this.showNotification('User banned successfully', 'success');
        this.loadStats();
      } else {
        this.showNotification('Failed to ban user', 'error');
      }
    } catch (error) {
      console.error('Error banning user:', error);
      this.showNotification('Error banning user', 'error');
    }
  }

  async deleteUser(userId) {
    if (!confirm('Are you sure you want to delete this user? This action cannot be undone.')) return;

    try {
      const response = await fetch(`/api/admin/users/${userId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (response.ok) {
        this.showNotification('User deleted successfully', 'success');
        this.loadStats();
      } else {
        this.showNotification('Failed to delete user', 'error');
      }
    } catch (error) {
      console.error('Error deleting user:', error);
      this.showNotification('Error deleting user', 'error');
    }
  }

  async createModule(formData) {
    try {
      const response = await fetch('/api/admin/modules', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        this.showNotification('Module created successfully', 'success');
        document.getElementById('module-form').reset();
      } else {
        this.showNotification('Failed to create module', 'error');
      }
    } catch (error) {
      console.error('Error creating module:', error);
      this.showNotification('Error creating module', 'error');
    }
  }

  async createChallenge(formData) {
    try {
      const response = await fetch('/api/admin/challenges', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        this.showNotification('Challenge created successfully', 'success');
        document.getElementById('challenge-form').reset();
      } else {
        this.showNotification('Failed to create challenge', 'error');
      }
    } catch (error) {
      console.error('Error creating challenge:', error);
      this.showNotification('Error creating challenge', 'error');
    }
  }

  showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Auto remove after 3 seconds
    setTimeout(() => {
      notification.remove();
    }, 3000);
  }
}

// Initialize admin dashboard
if (document.querySelector('.admin-dashboard')) {
  new AdminDashboard();
} 