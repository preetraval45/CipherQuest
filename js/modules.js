// ===== MODULES JAVASCRIPT =====

document.addEventListener('DOMContentLoaded', function() {
    initializeModules();
});

function initializeModules() {
    // Initialize view toggles
    initializeViewToggles();
    
    // Initialize filters
    initializeFilters();
    
    // Initialize module cards
    initializeModuleCards();
    
    // Initialize progress animations
    initializeProgressAnimations();
    
    // Initialize search functionality
    initializeSearch();
    
    // Initialize module interactions
    initializeModuleInteractions();
}

// ===== VIEW TOGGLES =====
function initializeViewToggles() {
    const viewButtons = document.querySelectorAll('.view-btn');
    const modulesGrid = document.getElementById('modulesGrid');
    
    viewButtons.forEach(button => {
        button.addEventListener('click', function() {
            const view = this.dataset.view;
            
            // Update active button
            viewButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Update grid view
            if (view === 'list') {
                modulesGrid.classList.add('list-view');
                animateToListView();
            } else {
                modulesGrid.classList.remove('list-view');
                animateToGridView();
            }
        });
    });
}

function animateToListView() {
    const cards = document.querySelectorAll('.module-card');
    
    gsap.to(cards, {
        duration: 0.5,
        scale: 1,
        ease: 'power2.out',
        stagger: 0.1
    });
}

function animateToGridView() {
    const cards = document.querySelectorAll('.module-card');
    
    gsap.to(cards, {
        duration: 0.5,
        scale: 1,
        ease: 'power2.out',
        stagger: 0.1
    });
}

// ===== FILTERS =====
function initializeFilters() {
    const difficultyFilter = document.getElementById('difficultyFilter');
    
    if (difficultyFilter) {
        difficultyFilter.addEventListener('change', function() {
            const selectedDifficulty = this.value;
            filterModules(selectedDifficulty);
        });
    }
}

function filterModules(difficulty) {
    const cards = document.querySelectorAll('.module-card');
    
    cards.forEach(card => {
        const cardDifficulty = card.dataset.difficulty;
        
        if (!difficulty || cardDifficulty === difficulty) {
            // Show card
            gsap.to(card, {
                duration: 0.3,
                opacity: 1,
                scale: 1,
                ease: 'power2.out'
            });
            card.classList.remove('filtered-out');
            card.classList.add('filtered-in');
        } else {
            // Hide card
            gsap.to(card, {
                duration: 0.3,
                opacity: 0.3,
                scale: 0.95,
                ease: 'power2.out'
            });
            card.classList.add('filtered-out');
            card.classList.remove('filtered-in');
        }
    });
}

// ===== MODULE CARDS =====
function initializeModuleCards() {
    const moduleCards = document.querySelectorAll('.module-card');
    
    // Animate cards on load
    gsap.from(moduleCards, {
        duration: 0.8,
        y: 50,
        opacity: 0,
        stagger: 0.1,
        ease: 'power3.out'
    });
    
    // Add hover effects
    moduleCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            gsap.to(this, {
                duration: 0.3,
                y: -10,
                scale: 1.02,
                ease: 'power2.out'
            });
            
            // Animate icon
            const icon = this.querySelector('.module-icon');
            if (icon) {
                gsap.to(icon, {
                    duration: 0.3,
                    rotation: 5,
                    scale: 1.1,
                    ease: 'power2.out'
                });
            }
        });
        
        card.addEventListener('mouseleave', function() {
            gsap.to(this, {
                duration: 0.3,
                y: 0,
                scale: 1,
                ease: 'power2.out'
            });
            
            // Reset icon
            const icon = this.querySelector('.module-icon');
            if (icon) {
                gsap.to(icon, {
                    duration: 0.3,
                    rotation: 0,
                    scale: 1,
                    ease: 'power2.out'
                });
            }
        });
    });
}

// ===== PROGRESS ANIMATIONS =====
function initializeProgressAnimations() {
    // Animate progress circle
    const progressCircle = document.querySelector('.progress-circle svg circle:last-child');
    if (progressCircle) {
        const circumference = 2 * Math.PI * 35;
        const progress = 50; // 50%
        const offset = circumference - (progress / 100) * circumference;
        
        progressCircle.style.strokeDasharray = circumference;
        progressCircle.style.strokeDashoffset = circumference;
        
        gsap.to(progressCircle, {
            duration: 2,
            strokeDashoffset: offset,
            ease: 'power2.out',
            delay: 0.5
        });
    }
    
    // Animate progress text
    const progressText = document.querySelector('.progress-text');
    if (progressText) {
        gsap.fromTo(progressText, {
            opacity: 0,
            scale: 0.8
        }, {
            duration: 1,
            opacity: 1,
            scale: 1,
            ease: 'back.out(1.7)',
            delay: 1.5
        });
    }
    
    // Animate stats
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach((stat, index) => {
        const finalValue = parseInt(stat.textContent.replace(/,/g, ''));
        
        gsap.fromTo(stat, {
            textContent: 0
        }, {
            duration: 2,
            textContent: finalValue,
            ease: 'power2.out',
            delay: 0.5 + (index * 0.2),
            snap: { textContent: 1 },
            onUpdate: function() {
                stat.textContent = parseInt(stat.textContent).toLocaleString();
            }
        });
    });
}

// ===== SEARCH FUNCTIONALITY =====
function initializeSearch() {
    // Add search input if not exists
    const topBarRight = document.querySelector('.top-bar-right');
    if (topBarRight && !document.querySelector('.search-container')) {
        const searchContainer = document.createElement('div');
        searchContainer.className = 'search-container';
        searchContainer.innerHTML = `
            <div class="search-wrapper">
                <i class="fas fa-search"></i>
                <input type="text" placeholder="Search modules..." id="moduleSearch">
            </div>
        `;
        
        topBarRight.insertBefore(searchContainer, topBarRight.firstChild);
        
        // Add search functionality
        const searchInput = document.getElementById('moduleSearch');
        searchInput.addEventListener('input', function() {
            searchModules(this.value);
        });
    }
}

function searchModules(query) {
    const cards = document.querySelectorAll('.module-card');
    const searchTerm = query.toLowerCase();
    
    cards.forEach(card => {
        const title = card.querySelector('h3').textContent.toLowerCase();
        const description = card.querySelector('p').textContent.toLowerCase();
        const category = card.querySelector('.category-tag').textContent.toLowerCase();
        
        if (title.includes(searchTerm) || 
            description.includes(searchTerm) || 
            category.includes(searchTerm)) {
            gsap.to(card, {
                duration: 0.3,
                opacity: 1,
                scale: 1,
                ease: 'power2.out'
            });
            card.style.display = 'block';
        } else {
            gsap.to(card, {
                duration: 0.3,
                opacity: 0,
                scale: 0.8,
                ease: 'power2.out',
                onComplete: () => {
                    card.style.display = 'none';
                }
            });
        }
    });
}

// ===== MODULE INTERACTIONS =====
function initializeModuleInteractions() {
    const moduleCards = document.querySelectorAll('.module-card');
    
    moduleCards.forEach(card => {
        const buttons = card.querySelectorAll('.btn');
        
        buttons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                
                const moduleName = card.querySelector('h3').textContent;
                const action = this.textContent.trim();
                
                if (action === 'Start Module' || action === 'Continue') {
                    startModule(moduleName, card);
                } else if (action === 'Review') {
                    reviewModule(moduleName, card);
                } else if (action === 'Preview') {
                    previewModule(moduleName, card);
                }
            });
        });
    });
}

function startModule(moduleName, card) {
    // Show loading state
    const button = card.querySelector('.btn-primary');
    const originalText = button.innerHTML;
    
    button.innerHTML = `
        <div class="loading-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    button.disabled = true;
    
    // Simulate module loading
    setTimeout(() => {
        showSuccessMessage(`Starting ${moduleName}...`);
        setTimeout(() => {
            // Redirect to module page (in real app)
            console.log(`Starting module: ${moduleName}`);
            button.innerHTML = originalText;
            button.disabled = false;
        }, 1500);
    }, 2000);
}

function reviewModule(moduleName, card) {
    showInfoMessage(`Opening review for ${moduleName}...`);
    // In real app, this would open a review modal or redirect
}

function previewModule(moduleName, card) {
    showInfoMessage(`Loading preview for ${moduleName}...`);
    // In real app, this would show a preview modal
}

// ===== MESSAGE HELPERS =====
function showSuccessMessage(message) {
    showMessage(message, 'success');
}

function showErrorMessage(message) {
    showMessage(message, 'error');
}

function showInfoMessage(message) {
    showMessage(message, 'info');
}

function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.module-message');
    existingMessages.forEach(msg => msg.remove());
    
    // Create message element
    const messageDiv = document.createElement('div');
    messageDiv.className = `module-message ${type}`;
    messageDiv.innerHTML = `
        <i class="fas fa-${getMessageIcon(type)}"></i>
        <span>${message}</span>
        <button class="close-message">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Add to page
    const modulesContent = document.querySelector('.modules-content');
    modulesContent.insertBefore(messageDiv, modulesContent.firstChild);
    
    // Animate in
    gsap.fromTo(messageDiv, {
        opacity: 0,
        y: -20
    }, {
        duration: 0.3,
        opacity: 1,
        y: 0,
        ease: 'power2.out'
    });
    
    // Close functionality
    const closeBtn = messageDiv.querySelector('.close-message');
    closeBtn.addEventListener('click', () => {
        gsap.to(messageDiv, {
            duration: 0.3,
            opacity: 0,
            y: -20,
            ease: 'power2.in',
            onComplete: () => messageDiv.remove()
        });
    });
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (messageDiv.parentNode) {
            gsap.to(messageDiv, {
                duration: 0.3,
                opacity: 0,
                y: -20,
                ease: 'power2.in',
                onComplete: () => messageDiv.remove()
            });
        }
    }, 5000);
}

function getMessageIcon(type) {
    switch (type) {
        case 'success': return 'check-circle';
        case 'error': return 'exclamation-circle';
        case 'info': return 'info-circle';
        default: return 'info-circle';
    }
}

// ===== UTILITY FUNCTIONS =====
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ===== EXPORT FOR MODULE USE =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeModules,
        filterModules,
        searchModules,
        startModule
    };
} 