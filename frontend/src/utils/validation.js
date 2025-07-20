// Form validation utility functions

/**
 * Validate email format
 * @param {string} email - Email to validate
 * @returns {boolean} True if email is valid
 */
export const validateEmail = (email) => {
  const emailRegex = /\S+@\S+\.\S+/;
  return emailRegex.test(email);
};

/**
 * Validate password strength
 * @param {string} password - Password to validate
 * @returns {Object} Validation result with isValid and message
 */
export const validatePassword = (password) => {
  if (!password) {
    return { isValid: false, message: 'Password is required' };
  }
  
  if (password.length < 6) {
    return { isValid: false, message: 'Password must be at least 6 characters' };
  }
  
  return { isValid: true, message: '' };
};

/**
 * Validate password confirmation
 * @param {string} password - Original password
 * @param {string} confirmPassword - Password confirmation
 * @returns {Object} Validation result with isValid and message
 */
export const validatePasswordConfirmation = (password, confirmPassword) => {
  if (password !== confirmPassword) {
    return { isValid: false, message: 'Passwords do not match' };
  }
  
  return { isValid: true, message: '' };
};

/**
 * Validate form data for authentication
 * @param {Object} formData - Form data object
 * @param {boolean} isLogin - Whether this is a login form
 * @returns {Object} Validation result with errors object
 */
export const validateAuthForm = (formData, isLogin = true) => {
  const errors = {};

  // Email validation
  if (!formData.email) {
    errors.email = 'Email is required';
  } else if (!validateEmail(formData.email)) {
    errors.email = 'Email is invalid';
  }

  // Password validation
  const passwordValidation = validatePassword(formData.password);
  if (!passwordValidation.isValid) {
    errors.password = passwordValidation.message;
  }

  // Password confirmation validation (only for signup)
  if (!isLogin && formData.confirmPassword) {
    const confirmValidation = validatePasswordConfirmation(formData.password, formData.confirmPassword);
    if (!confirmValidation.isValid) {
      errors.confirmPassword = confirmValidation.message;
    }
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};

/**
 * Clear specific field error when user starts typing
 * @param {Object} errors - Current errors object
 * @param {string} fieldName - Field name to clear error for
 * @returns {Object} Updated errors object
 */
export const clearFieldError = (errors, fieldName) => {
  if (errors[fieldName]) {
    const newErrors = { ...errors };
    delete newErrors[fieldName];
    return newErrors;
  }
  return errors;
}; 