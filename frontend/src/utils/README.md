# Frontend Utilities

This directory contains common utility functions used throughout the CipherQuest frontend application.

## Structure

```
utils/
├── index.js          # Main export file
├── auth.js           # Authentication utilities
├── validation.js     # Form validation utilities
├── api.js            # API request utilities
├── ui.js             # UI helper functions
├── datetime.js       # Date and time utilities
└── README.md         # This file
```

## Usage

Import utilities from the main index file:

```javascript
import { validateEmail, formatXP, getAuthToken } from '../utils';
```

Or import specific utilities:

```javascript
import { validateEmail } from '../utils/validation';
import { formatXP } from '../utils/ui';
import { getAuthToken } from '../utils/auth';
```

## Authentication Utilities (`auth.js`)

### Functions

- `storeAuthToken(token)` - Store JWT token in localStorage
- `getAuthToken()` - Retrieve JWT token from localStorage
- `removeAuthToken()` - Remove JWT token from localStorage
- `isAuthenticated()` - Check if user has valid token
- `authenticateUser(credentials, isLogin)` - Simulate authentication API call
- `handleAuthError(error)` - Handle authentication errors

### Example

```javascript
import { storeAuthToken, isAuthenticated } from '../utils/auth';

// Store token after login
storeAuthToken('jwt-token-here');

// Check if user is logged in
if (isAuthenticated()) {
  // User is authenticated
}
```

## Validation Utilities (`validation.js`)

### Functions

- `validateEmail(email)` - Validate email format
- `validatePassword(password)` - Validate password strength
- `validatePasswordConfirmation(password, confirmPassword)` - Validate password confirmation
- `validateAuthForm(formData, isLogin)` - Validate authentication form
- `clearFieldError(errors, fieldName)` - Clear specific field error

### Example

```javascript
import { validateEmail, validateAuthForm } from '../utils/validation';

// Validate email
if (!validateEmail(email)) {
  setError('Invalid email format');
}

// Validate form
const validation = validateAuthForm(formData, true);
if (!validation.isValid) {
  setErrors(validation.errors);
}
```

## API Utilities (`api.js`)

### Functions

- `apiRequest(endpoint, options)` - Make authenticated API request
- `apiGet(endpoint, options)` - GET request
- `apiPost(endpoint, data, options)` - POST request
- `apiPut(endpoint, data, options)` - PUT request
- `apiDelete(endpoint, options)` - DELETE request
- `handleApiError(error)` - Handle API errors

### Example

```javascript
import { apiGet, apiPost, handleApiError } from '../utils/api';

// Get user profile
try {
  const profile = await apiGet('/user/profile');
  setUser(profile);
} catch (error) {
  const message = handleApiError(error);
  showError(message);
}

// Create new module
const moduleData = { title: 'New Module', content: '...' };
const newModule = await apiPost('/modules', moduleData);
```

## UI Utilities (`ui.js`)

### Functions

- `getActivityIcon(type)` - Get emoji icon for activity type
- `getStatusColor(status)` - Get CSS color for status
- `getDifficultyColor(difficulty)` - Get CSS color for difficulty
- `formatNumber(number)` - Format number with locale
- `formatXP(xp)` - Format XP with appropriate suffix
- `getRankBadge(rank)` - Get rank badge emoji
- `randomDelay(min, max)` - Generate random loading delay
- `debounce(func, wait)` - Debounce function calls

### Example

```javascript
import { getActivityIcon, formatXP, getRankBadge } from '../utils/ui';

// Display activity icon
const icon = getActivityIcon('module'); // Returns '📚'

// Format XP display
const xpDisplay = formatXP(1500); // Returns '1.5K XP'

// Display rank badge
const badge = getRankBadge(1); // Returns '🥇'
```

## Date/Time Utilities (`datetime.js`)

### Functions

- `formatRelativeTime(date)` - Format relative time (e.g., "2 hours ago")
- `formatDate(date, locale)` - Format date in readable format
- `formatDateTime(date, locale)` - Format date and time
- `isToday(date)` - Check if date is today
- `isYesterday(date)` - Check if date is yesterday
- `getTimeUntil(targetDate)` - Get time until target date
- `formatDuration(seconds)` - Format duration in human readable format

### Example

```javascript
import { formatRelativeTime, formatDate } from '../utils/datetime';

// Format relative time
const timeAgo = formatRelativeTime('2023-01-15T10:30:00Z');
// Returns "2 hours ago"

// Format date
const date = formatDate('2023-01-15');
// Returns "January 15, 2023"
```

## Best Practices

1. **Import from index**: Use the main index file for imports to maintain clean imports
2. **Error handling**: Always handle errors when using API utilities
3. **Validation**: Use validation utilities for all form inputs
4. **Consistency**: Use UI utilities for consistent formatting across the app
5. **Testing**: All utilities should be unit tested

## Adding New Utilities

When adding new utility functions:

1. Create a new file in the appropriate category
2. Export functions from the file
3. Add exports to `index.js`
4. Update this README with documentation
5. Write unit tests for the new functions

## Testing

Utilities can be tested independently:

```javascript
import { validateEmail } from '../utils/validation';

describe('validateEmail', () => {
  it('should validate correct email', () => {
    expect(validateEmail('test@example.com')).toBe(true);
  });
  
  it('should reject invalid email', () => {
    expect(validateEmail('invalid-email')).toBe(false);
  });
});
``` 