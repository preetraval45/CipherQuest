// ===== MAIN JAVASCRIPT =====

document.addEventListener('DOMContentLoaded', function() {
    // Initialize GSAP animations
    initializeAnimations();
    
    // Initialize navigation
    initializeNavigation();
    
    // Initialize interactive elements
    initializeInteractiveElements();
    
    // Initialize scroll animations
    initializeScrollAnimations();
});

// ===== ANIMATION INITIALIZATION =====
function initializeAnimations() {
    // Hero section animations
    const heroTimeline = gsap.timeline();
    
    heroTimeline
        .from('.hero-title', {
            duration: 1,
            y: 50,
            opacity: 0,
            ease: 'power3.out'
        })
        .from('.hero-subtitle', {
            duration: 0.8,
            y: 30,
            opacity: 0,
            ease: 'power3.out'
        }, '-=0.5')
        .from('.hero-buttons', {
            duration: 0.8,
            y: 30,
            opacity: 0,
            ease: 'power3.out'
        }, '-=0.3')
        .from('.cyber-cube', {
            duration: 1.2,
            rotation: 360,
            scale: 0,
            opacity: 0,
            ease: 'back.out(1.7)'
        }, '-=0.5');

    // Feature cards animation
    gsap.from('.feature-card', {
        duration: 0.8,
        y: 50,
        opacity: 0,
        stagger: 0.2,
        ease: 'power3.out',
        scrollTrigger: {
            trigger: '.features-grid',
            start: 'top 80%',
            end: 'bottom 20%',
            toggleActions: 'play none none reverse'
        }
    });

    // Floating particles animation
    animateFloatingParticles();
}

// ===== NAVIGATION INITIALIZATION =====
function initializeNavigation() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
    }

    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Navbar background on scroll
    window.addEventListener('scroll', function() {
        const navbar = document.querySelector('.navbar');
        if (window.scrollY > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
}

// ===== INTERACTIVE ELEMENTS =====
function initializeInteractiveElements() {
    // Button hover effects
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            gsap.to(this, {
                duration: 0.3,
                scale: 1.05,
                ease: 'power2.out'
            });
        });
        
        button.addEventListener('mouseleave', function() {
            gsap.to(this, {
                duration: 0.3,
                scale: 1,
                ease: 'power2.out'
            });
        });
    });

    // Feature card interactions
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            gsap.to(this, {
                duration: 0.3,
                y: -10,
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
    });

    // Video placeholder interaction
    const videoPlaceholder = document.querySelector('.video-placeholder');
    if (videoPlaceholder) {
        videoPlaceholder.addEventListener('click', function() {
            // Simulate video play
            this.innerHTML = `
                <div class="video-playing">
                    <i class="fas fa-play"></i>
                    <p>Video Playing...</p>
                </div>
            `;
            
            // Add playing animation
            gsap.to(this, {
                duration: 0.5,
                scale: 1.05,
                ease: 'power2.out'
            });
        });
    }
}

// ===== SCROLL ANIMATIONS =====
function initializeScrollAnimations() {
    // Animate elements on scroll
    const animateElements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                gsap.from(entry.target, {
                    duration: 0.8,
                    y: 50,
                    opacity: 0,
                    ease: 'power3.out'
                });
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    animateElements.forEach(el => observer.observe(el));
}

// ===== FLOATING PARTICLES =====
function animateFloatingParticles() {
    const particles = document.querySelector('.floating-particles');
    if (!particles) return;

    // Create additional particles
    for (let i = 0; i < 10; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: 2px;
            height: 2px;
            background: var(--primary-color);
            border-radius: 50%;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
            opacity: ${Math.random() * 0.5 + 0.3};
        `;
        particles.appendChild(particle);

        // Animate particle
        gsap.to(particle, {
            duration: Math.random() * 10 + 10,
            y: -100,
            x: Math.random() * 50 - 25,
            opacity: 0,
            ease: 'none',
            repeat: -1,
            delay: Math.random() * 5
        });
    }
}

// ===== GLITCH EFFECT =====
function initializeGlitchEffect() {
    const glitchElements = document.querySelectorAll('.glitch');
    
    glitchElements.forEach(element => {
        setInterval(() => {
            if (Math.random() > 0.95) {
                element.style.transform = `translate(${Math.random() * 4 - 2}px, ${Math.random() * 4 - 2}px)`;
                element.style.textShadow = `
                    ${Math.random() * 4 - 2}px 0 var(--secondary-color),
                    ${Math.random() * 4 - 2}px 0 var(--accent-color)
                `;
                
                setTimeout(() => {
                    element.style.transform = '';
                    element.style.textShadow = '';
                }, 100);
            }
        }, 50);
    });
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

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ===== PERFORMANCE OPTIMIZATION =====
const optimizedScrollHandler = throttle(function() {
    // Handle scroll events efficiently
}, 16);

window.addEventListener('scroll', optimizedScrollHandler);

// ===== ERROR HANDLING =====
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
});

// ===== INITIALIZE GLITCH EFFECT =====
setTimeout(initializeGlitchEffect, 1000);

// ===== EXPORT FOR MODULE USE =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeAnimations,
        initializeNavigation,
        initializeInteractiveElements,
        initializeScrollAnimations
    };
} 