// ===== DASHBOARD JAVASCRIPT =====

document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

function initializeDashboard() {
    // Initialize sidebar navigation
    initializeSidebar();
    
    // Initialize progress animations
    initializeProgressAnimations();
    
    // Initialize leaderboard
    initializeLeaderboard();
    
    // Initialize notifications
    initializeNotifications();
    
    // Initialize user menu
    initializeUserMenu();
    
    // Initialize challenge cards
    initializeChallengeCards();
    
    // Initialize activity feed
    initializeActivityFeed();
}

// ===== SIDEBAR NAVIGATION =====
function initializeSidebar() {
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
            mainContent.classList.toggle('sidebar-active');
        });
    }
    
    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 1024) {
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                sidebar.classList.remove('active');
                mainContent.classList.remove('sidebar-active');
            }
        }
    });
    
    // Handle sidebar link clicks
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    sidebarLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Remove active class from all links
            sidebarLinks.forEach(l => l.classList.remove('active'));
            // Add active class to clicked link
            this.classList.add('active');
        });
    });
}

// ===== PROGRESS ANIMATIONS =====
function initializeProgressAnimations() {
    // Animate progress bars on load
    const progressBars = document.querySelectorAll('.progress-fill');
    
    progressBars.forEach(bar => {
        const targetWidth = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            gsap.to(bar, {
                duration: 1.5,
                width: targetWidth,
                ease: 'power2.out'
            });
        }, 500);
    });
    
    // Animate progress circle
    const progressCircle = document.querySelector('.progress-circle circle:last-child');
    if (progressCircle) {
        const circumference = 2 * Math.PI * 35; // radius = 35
        const progress = 50; // 50%
        const offset = circumference - (progress / 100) * circumference;
        
        progressCircle.style.strokeDasharray = circumference;
        progressCircle.style.strokeDashoffset = circumference;
        
        gsap.to(progressCircle, {
            duration: 2,
            strokeDashoffset: offset,
            ease: 'power2.out'
        });
    }
    
    // Animate stat numbers
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(stat => {
        const finalValue = parseInt(stat.textContent.replace(/,/g, ''));
        const startValue = 0;
        
        gsap.fromTo(stat, {
            textContent: startValue
        }, {
            duration: 2,
            textContent: finalValue,
            ease: 'power2.out',
            snap: { textContent: 1 },
            onUpdate: function() {
                stat.textContent = parseInt(stat.textContent).toLocaleString();
            }
        });
    });
}

// ===== LEADERBOARD =====
function initializeLeaderboard() {
    const leaderboardItems = document.querySelectorAll('.leaderboard-item');
    
    // Animate leaderboard items on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                gsap.fromTo(entry.target, {
                    opacity: 0,
                    x: -50
                }, {
                    duration: 0.5,
                    opacity: 1,
                    x: 0,
                    delay: index * 0.1,
                    ease: 'power2.out'
                });
            }
        });
    }, {
        threshold: 0.1
    });
    
    leaderboardItems.forEach(item => observer.observe(item));
    
    // Add hover effects
    leaderboardItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            gsap.to(this, {
                duration: 0.3,
                scale: 1.02,
                ease: 'power2.out'
            });
        });
        
        item.addEventListener('mouseleave', function() {
            gsap.to(this, {
                duration: 0.3,
                scale: 1,
                ease: 'power2.out'
            });
        });
    });
}

// ===== NOTIFICATIONS =====
function initializeNotifications() {
    const notificationBtn = document.querySelector('.notifications');
    const notificationBadge = document.querySelector('.notification-badge');
    
    if (notificationBtn) {
        notificationBtn.addEventListener('click', function() {
            showNotificationsPanel();
        });
    }
    
    // Simulate new notifications
    setInterval(() => {
        if (Math.random() > 0.95) {
            addNotification();
        }
    }, 30000);
}

function showNotificationsPanel() {
    // Create notifications panel
    const panel = document.createElement('div');
    panel.className = 'notifications-panel';
    panel.innerHTML = `
        <div class="notifications-header">
            <h3>Notifications</h3>
            <button class="close-btn">
                <i class="fas fa-times"></i>
            </button>
        </div>
        <div class="notifications-list">
            <div class="notification-item">
                <i class="fas fa-trophy"></i>
                <div class="notification-content">
                    <p>Congratulations! You've earned the "Web Warrior" badge!</p>
                    <span>2 minutes ago</span>
                </div>
            </div>
            <div class="notification-item">
                <i class="fas fa-star"></i>
                <div class="notification-content">
                    <p>New challenge available: "Advanced SQL Injection"</p>
                    <span>1 hour ago</span>
                </div>
            </div>
            <div class="notification-item">
                <i class="fas fa-users"></i>
                <div class="notification-content">
                    <p>You've been challenged by "ByteMaster"</p>
                    <span>3 hours ago</span>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(panel);
    
    // Animate in
    gsap.fromTo(panel, {
        opacity: 0,
        scale: 0.8
    }, {
        duration: 0.3,
        opacity: 1,
        scale: 1,
        ease: 'back.out(1.7)'
    });
    
    // Close functionality
    const closeBtn = panel.querySelector('.close-btn');
    closeBtn.addEventListener('click', () => {
        gsap.to(panel, {
            duration: 0.3,
            opacity: 0,
            scale: 0.8,
            ease: 'back.in(1.7)',
            onComplete: () => panel.remove()
        });
    });
}

function addNotification() {
    const badge = document.querySelector('.notification-badge');
    if (badge) {
        const currentCount = parseInt(badge.textContent);
        badge.textContent = currentCount + 1;
        
        // Animate badge
        gsap.to(badge, {
            duration: 0.2,
            scale: 1.3,
            ease: 'power2.out',
            yoyo: true,
            repeat: 1
        });
    }
}

// ===== USER MENU =====
function initializeUserMenu() {
    const userMenu = document.querySelector('.user-menu');
    
    if (userMenu) {
        userMenu.addEventListener('click', function() {
            showUserMenu();
        });
    }
}

function showUserMenu() {
    const menu = document.createElement('div');
    menu.className = 'user-dropdown';
    menu.innerHTML = `
        <div class="dropdown-item">
            <i class="fas fa-user"></i>
            <span>Profile</span>
        </div>
        <div class="dropdown-item">
            <i class="fas fa-cog"></i>
            <span>Settings</span>
        </div>
        <div class="dropdown-item">
            <i class="fas fa-question-circle"></i>
            <span>Help</span>
        </div>
        <div class="dropdown-divider"></div>
        <div class="dropdown-item">
            <i class="fas fa-sign-out-alt"></i>
            <span>Logout</span>
        </div>
    `;
    
    const userMenu = document.querySelector('.user-menu');
    userMenu.appendChild(menu);
    
    // Position menu
    const rect = userMenu.getBoundingClientRect();
    menu.style.position = 'absolute';
    menu.style.top = '100%';
    menu.style.right = '0';
    menu.style.zIndex = '1000';
    
    // Animate in
    gsap.fromTo(menu, {
        opacity: 0,
        y: -10
    }, {
        duration: 0.2,
        opacity: 1,
        y: 0,
        ease: 'power2.out'
    });
    
    // Close on outside click
    document.addEventListener('click', function closeMenu(e) {
        if (!userMenu.contains(e.target)) {
            gsap.to(menu, {
                duration: 0.2,
                opacity: 0,
                y: -10,
                ease: 'power2.in',
                onComplete: () => menu.remove()
            });
            document.removeEventListener('click', closeMenu);
        }
    });
}

// ===== CHALLENGE CARDS =====
function initializeChallengeCards() {
    const challengeCards = document.querySelectorAll('.challenge-card');
    
    challengeCards.forEach(card => {
        // Add hover effects
        card.addEventListener('mouseenter', function() {
            gsap.to(this, {
                duration: 0.3,
                y: -5,
                scale: 1.02,
                ease: 'power2.out'
            });
        });
        
        card.addEventListener('mouseleave', function() {
            gsap.to(this, {
                duration: 0.3,
                y: 0,
                scale: 1,
                ease: 'power2.out'
            });
        });
        
        // Add click handlers
        const startBtn = card.querySelector('.btn');
        if (startBtn) {
            startBtn.addEventListener('click', function() {
                const challengeName = card.querySelector('h3').textContent;
                startChallenge(challengeName);
            });
        }
    });
}

function startChallenge(challengeName) {
    // Show loading state
    showLoadingOverlay(`Starting ${challengeName}...`);
    
    // Simulate challenge loading
    setTimeout(() => {
        hideLoadingOverlay();
        // Redirect to challenge page (in real app)
        console.log(`Starting challenge: ${challengeName}`);
    }, 2000);
}

// ===== ACTIVITY FEED =====
function initializeActivityFeed() {
    const activityItems = document.querySelectorAll('.activity-item');
    
    // Animate activity items on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                gsap.fromTo(entry.target, {
                    opacity: 0,
                    x: 50
                }, {
                    duration: 0.5,
                    opacity: 1,
                    x: 0,
                    delay: index * 0.1,
                    ease: 'power2.out'
                });
            }
        });
    }, {
        threshold: 0.1
    });
    
    activityItems.forEach(item => observer.observe(item));
}

// ===== LOADING OVERLAY =====
function showLoadingOverlay(message) {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.innerHTML = `
        <div class="loading-content">
            <div class="loading-spinner"></div>
            <p>${message}</p>
        </div>
    `;
    
    document.body.appendChild(overlay);
    
    gsap.fromTo(overlay, {
        opacity: 0
    }, {
        duration: 0.3,
        opacity: 1,
        ease: 'power2.out'
    });
}

function hideLoadingOverlay() {
    const overlay = document.querySelector('.loading-overlay');
    if (overlay) {
        gsap.to(overlay, {
            duration: 0.3,
            opacity: 0,
            ease: 'power2.in',
            onComplete: () => overlay.remove()
        });
    }
}

// ===== UTILITY FUNCTIONS =====
function formatNumber(num) {
    return num.toLocaleString();
}

function formatTimeAgo(timestamp) {
    const now = new Date();
    const time = new Date(timestamp);
    const diff = now - time;
    
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);
    
    if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
    if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
    if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
    return 'Just now';
}

// ===== EXPORT FOR MODULE USE =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeDashboard,
        initializeSidebar,
        initializeProgressAnimations,
        initializeLeaderboard,
        startChallenge
    };
} 