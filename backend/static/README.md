# Backend Static Files

This directory contains static files served by the Flask backend application.

## Structure

```
static/
├── css/
│   └── style.css          # Main backend styles
├── js/
│   └── admin.js           # Admin panel JavaScript
├── images/
│   └── logo.png           # Application logo
├── favicon.ico            # Browser favicon
└── README.md              # This file
```

## Usage

Static files are served by Flask at the `/static/` URL path. For example:

- CSS: `http://localhost:5000/static/css/style.css`
- JavaScript: `http://localhost:5000/static/js/admin.js`
- Images: `http://localhost:5000/static/images/logo.png`
- Favicon: `http://localhost:5000/static/favicon.ico`

## CSS Files

### `css/style.css`

Contains styles for:
- Error pages (404, 500, etc.)
- API documentation pages
- Admin panel styling
- Loading spinners and animations
- Base layout and typography

## JavaScript Files

### `js/admin.js`

Contains functionality for:
- Admin dashboard interactions
- User management (ban, delete)
- Module and challenge creation
- Statistics display
- Form handling and validation

## Images

### `images/logo.png`

The CipherQuest application logo. Replace this placeholder with the actual logo file.

## Favicon

### `favicon.ico`

Browser favicon for the application. Replace this placeholder with the actual favicon file.

## Adding New Static Files

When adding new static files:

1. **CSS**: Add to `css/` directory and reference in HTML templates
2. **JavaScript**: Add to `js/` directory and include in HTML templates
3. **Images**: Add to `images/` directory and reference with `/static/images/filename`
4. **Other files**: Add to appropriate subdirectory

## Flask Configuration

The Flask app is configured to serve static files from this directory:

```python
app = Flask(__name__, static_folder='static', static_url_path='/static')
```

## Development

During development, static files are served directly by Flask. For production:

1. Consider using a CDN for better performance
2. Implement caching headers for static assets
3. Minify CSS and JavaScript files
4. Optimize images for web delivery

## Security

- Static files are publicly accessible
- Don't store sensitive information in static files
- Use proper file permissions
- Validate file uploads if implementing file upload functionality

## Best Practices

1. **Organization**: Keep files organized in appropriate subdirectories
2. **Naming**: Use descriptive, lowercase filenames with hyphens
3. **Versioning**: Consider versioning static assets for cache busting
4. **Minification**: Minify CSS and JS files for production
5. **Compression**: Enable gzip compression for static files 