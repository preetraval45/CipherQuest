// ===== AUTHENTICATION JAVASCRIPT =====

document.addEventListener('DOMContentLoaded', function() {
    initializeAuth();
});

function initializeAuth() {
    // Initialize form handling
    initializeForms();
    
    // Initialize password toggles
    initializePasswordToggles();
    
    // Initialize OAuth buttons
    initializeOAuthButtons();
    
    // Initialize form switching
    initializeFormSwitching();
    
    // Initialize form validation
    initializeFormValidation();
}

// ===== FORM HANDLING =====
function initializeForms() {
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
    }
}

function handleLogin(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('.btn');
    const email = form.querySelector('#email').value;
    const password = form.querySelector('#password').value;
    const remember = form.querySelector('#remember').checked;
    
    // Show loading state
    setButtonLoading(submitBtn, true);
    
    // Simulate API call
    setTimeout(() => {
        if (validateLoginForm(email, password)) {
            // Simulate successful login
            showSuccessMessage('Login successful! Redirecting...');
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1500);
        } else {
            showErrorMessage('Invalid email or password');
            setButtonLoading(submitBtn, false);
        }
    }, 2000);
}

function handleSignup(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('.btn');
    const name = form.querySelector('#signupName').value;
    const email = form.querySelector('#signupEmail').value;
    const password = form.querySelector('#signupPassword').value;
    const confirmPassword = form.querySelector('#confirmPassword').value;
    const terms = form.querySelector('#terms').checked;
    
    // Show loading state
    setButtonLoading(submitBtn, true);
    
    // Simulate API call
    setTimeout(() => {
        if (validateSignupForm(name, email, password, confirmPassword, terms)) {
            // Simulate successful signup
            showSuccessMessage('Account created successfully! Redirecting...');
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1500);
        } else {
            showErrorMessage('Please check your input and try again');
            setButtonLoading(submitBtn, false);
        }
    }, 2000);
}

// ===== PASSWORD TOGGLES =====
function initializePasswordToggles() {
    const toggleButtons = document.querySelectorAll('.toggle-password');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const input = this.parentElement.querySelector('input');
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.className = 'fas fa-eye-slash';
            } else {
                input.type = 'password';
                icon.className = 'fas fa-eye';
            }
        });
    });
}

// ===== OAUTH BUTTONS =====
function initializeOAuthButtons() {
    const oauthButtons = document.querySelectorAll('.oauth-btn');
    
    oauthButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const provider = this.classList.contains('google') ? 'Google' : 'GitHub';
            
            // Show loading state
            const originalText = this.innerHTML;
            this.innerHTML = `
                <div class="loading-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            `;
            this.disabled = true;
            
            // Simulate OAuth flow
            setTimeout(() => {
                showSuccessMessage(`${provider} authentication successful!`);
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 1500);
            }, 2000);
        });
    });
}

// ===== FORM SWITCHING =====
function initializeFormSwitching() {
    const showSignupBtn = document.getElementById('showSignup');
    const showLoginBtn = document.getElementById('showLogin');
    const loginCard = document.querySelector('.auth-card:not(.signup-card)');
    const signupCard = document.querySelector('.signup-card');
    
    if (showSignupBtn && showLoginBtn) {
        showSignupBtn.addEventListener('click', function(e) {
            e.preventDefault();
            switchToSignup();
        });
        
        showLoginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            switchToLogin();
        });
    }
}

function switchToSignup() {
    const loginCard = document.querySelector('.auth-card:not(.signup-card)');
    const signupCard = document.querySelector('.signup-card');
    
    if (loginCard && signupCard) {
        // Animate out login card
        gsap.to(loginCard, {
            duration: 0.3,
            opacity: 0,
            x: -50,
            ease: 'power2.inOut',
            onComplete: () => {
                loginCard.style.display = 'none';
                signupCard.style.display = 'block';
                
                // Animate in signup card
                gsap.fromTo(signupCard, {
                    opacity: 0,
                    x: 50
                }, {
                    duration: 0.3,
                    opacity: 1,
                    x: 0,
                    ease: 'power2.inOut'
                });
            }
        });
    }
}

function switchToLogin() {
    const loginCard = document.querySelector('.auth-card:not(.signup-card)');
    const signupCard = document.querySelector('.signup-card');
    
    if (loginCard && signupCard) {
        // Animate out signup card
        gsap.to(signupCard, {
            duration: 0.3,
            opacity: 0,
            x: 50,
            ease: 'power2.inOut',
            onComplete: () => {
                signupCard.style.display = 'none';
                loginCard.style.display = 'block';
                
                // Animate in login card
                gsap.fromTo(loginCard, {
                    opacity: 0,
                    x: -50
                }, {
                    duration: 0.3,
                    opacity: 1,
                    x: 0,
                    ease: 'power2.inOut'
                });
            }
        });
    }
}

// ===== FORM VALIDATION =====
function initializeFormValidation() {
    const inputs = document.querySelectorAll('.input-wrapper input');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            clearFieldError(this);
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    
    // Remove existing error state
    clearFieldError(field);
    
    // Validate based on field type
    switch (fieldName) {
        case 'email':
            if (!isValidEmail(value)) {
                showFieldError(field, 'Please enter a valid email address');
            }
            break;
        case 'password':
            if (value.length < 6) {
                showFieldError(field, 'Password must be at least 6 characters');
            }
            break;
        case 'confirmPassword':
            const password = document.querySelector('#signupPassword').value;
            if (value !== password) {
                showFieldError(field, 'Passwords do not match');
            }
            break;
        case 'name':
            if (value.length < 2) {
                showFieldError(field, 'Name must be at least 2 characters');
            }
            break;
    }
}

function validateLoginForm(email, password) {
    // Simple validation for demo
    return email.length > 0 && password.length > 0;
}

function validateSignupForm(name, email, password, confirmPassword, terms) {
    return name.length > 0 && 
           isValidEmail(email) && 
           password.length >= 6 && 
           password === confirmPassword && 
           terms;
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function showFieldError(field, message) {
    const formGroup = field.closest('.form-group');
    formGroup.classList.add('error');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    formGroup.appendChild(errorDiv);
}

function clearFieldError(field) {
    const formGroup = field.closest('.form-group');
    formGroup.classList.remove('error');
    
    const errorMessage = formGroup.querySelector('.error-message');
    if (errorMessage) {
        errorMessage.remove();
    }
}

// ===== UI HELPERS =====
function setButtonLoading(button, loading) {
    if (loading) {
        button.classList.add('loading');
        button.disabled = true;
    } else {
        button.classList.remove('loading');
        button.disabled = false;
    }
}

function showSuccessMessage(message) {
    showMessage(message, 'success');
}

function showErrorMessage(message) {
    showMessage(message, 'error');
}

function showMessage(message, type) {
    // Remove existing messages
    const existingMessages = document.querySelectorAll('.auth-message');
    existingMessages.forEach(msg => msg.remove());
    
    // Create new message
    const messageDiv = document.createElement('div');
    messageDiv.className = `auth-message ${type}`;
    messageDiv.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add to page
    const authContainer = document.querySelector('.auth-container');
    authContainer.appendChild(messageDiv);
    
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
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        gsap.to(messageDiv, {
            duration: 0.3,
            opacity: 0,
            y: -20,
            ease: 'power2.in',
            onComplete: () => messageDiv.remove()
        });
    }, 5000);
}

// ===== FORGOT PASSWORD =====
function initializeForgotPassword() {
    const forgotPasswordLink = document.querySelector('.forgot-password');
    
    if (forgotPasswordLink) {
        forgotPasswordLink.addEventListener('click', function(e) {
            e.preventDefault();
            
            const email = document.querySelector('#email').value;
            if (email && isValidEmail(email)) {
                showSuccessMessage('Password reset link sent to your email!');
            } else {
                showErrorMessage('Please enter a valid email address first');
            }
        });
    }
}

// ===== INITIALIZE FORGOT PASSWORD =====
setTimeout(initializeForgotPassword, 100);

// ===== EXPORT FOR MODULE USE =====
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeAuth,
        handleLogin,
        handleSignup,
        validateField,
        showMessage
    };
} 