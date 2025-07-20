# CipherQuest - Hack. Learn. Level Up

[![Build Status](https://github.com/preetraval45/CipherQuest/actions/workflows/ci.yml/badge.svg)](https://github.com/preetraval45/CipherQuest/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Coverage Status](https://img.shields.io/badge/coverage-unknown-lightgrey)](https://github.com/preetraval45/CipherQuest)

A modern, cyberpunk-themed cybersecurity learning platform built with HTML, CSS, and JavaScript.

## 🎯 Overview

CipherQuest is an immersive cybersecurity education platform that combines gamified learning with AI-powered tutoring. The platform features a sleek cyberpunk design with glassmorphism effects, neon glows, and smooth animations.

## ✨ Features

### 🏠 Landing Page

- **Hero Section**: Animated 3D cyber cube with glitch text effects
- **Video Section**: Embedded platform introduction video
- **Features Grid**: Interactive feature cards with hover animations
- **Responsive Design**: Mobile-first approach with smooth transitions

### 🔐 Authentication

- **Login/Signup Forms**: Clean, minimal UI with glassmorphism effects
- **OAuth Integration**: Google and GitHub authentication options
- **Form Validation**: Real-time validation with error handling
- **Password Toggle**: Show/hide password functionality
- **Smooth Transitions**: Animated form switching

### 📊 Dashboard

- **User Profile Card**: XP, rank, badges, and progress tracking
- **Quick Stats**: Real-time statistics with animated counters
- **Activity Feed**: Recent user activity with status indicators
- **Leaderboard**: Animated top hackers ranking
- **Recommended Challenges**: Personalized challenge suggestions

### 📚 Learning Modules

- **Module Grid/List View**: Toggle between grid and list layouts
- **Difficulty Filtering**: Filter modules by difficulty level
- **Progress Tracking**: Visual progress indicators
- **Module Cards**: Animated cards with tilt effects and glows
- **Prerequisites**: Module dependency system

### 🤖 AI Tutor

- **Chat Interface**: Cyber terminal-styled chat
- **Typing Effects**: Animated AI response typing
- **Voice Controls**: Speech-to-text functionality
- **Quick Actions**: Pre-defined learning prompts
- **Code Highlighting**: Syntax-highlighted code blocks
- **Chat Export**: Export conversation history

## 🎨 Design System

### Color Palette

- **Primary**: `#00ff88` (Cyber Green)
- **Secondary**: `#ff0080` (Neon Pink)
- **Accent**: `#0080ff` (Electric Blue)
- **Background**: `#0a0a0a` (Dark)
- **Surface**: `rgba(255, 255, 255, 0.05)` (Glass)

### Typography

- **Primary**: Orbitron (Headings)
- **Secondary**: Fira Code (Code/Monospace)
- **Body**: Montserrat (Body text)

### Effects

- **Glassmorphism**: Backdrop blur with transparency
- **Neon Glows**: CSS box-shadows with color
- **Smooth Animations**: GSAP-powered transitions
- **Hover Effects**: Scale, rotation, and glow animations

## 🚀 Getting Started

### Prerequisites

- Modern web browser (Chrome, Firefox, Safari, Edge)
- Local web server (optional, for development)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/cipherquest.git
   cd cipherquest
   ```

2. **Open in browser**
   - Simply open `index.html` in your browser
   - Or use a local server for better development experience

3. **Using a local server (recommended)**

   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js (if you have http-server installed)
   npx http-server
   
   # Using PHP
   php -S localhost:8000
   ```

4. **Access the application**
   - Navigate to `http://localhost:8000`
   - The application will load with all features

## 📁 Project Structure

CipherQuest/
├── assets/
│   ├── fonts/
│   └── images/
├── backend/
│   ├── app.py
│   ├── CipherQuest_API.postman_collection.json
│   ├── config.py
│   ├── env.example
│   ├── init_db.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── challenge.py
│   │   ├── leaderboard.py
│   │   ├── module.py
│   │   ├── progress.py
│   │   └── user.py
│   ├── README.md
│   ├── requirements.txt
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── challenges.py
│   │   ├── leaderboard.py
│   │   ├── modules.py
│   │   └── user.py
│   ├── run.py
│   ├── setup.py
│   └── utils/
│       ├── __init__.py
│       └── validators.py
├── css/
│   ├── animations.css
│   ├── auth.css
│   ├── dashboard.css
│   ├── modules.css
│   └── style.css
├── docs/
├── frontend/
│   ├── package-lock.json
│   ├── package.json
│   ├── public/
│   ├── README.md
│   └── src/
│       ├── App.css
│       ├── App.js
│       ├── components/
│       │   ├── auth/
│       │   │   └── ProtectedRoute.js
│       │   └── layout/
│       │       ├── Layout.css
│       │       └── Layout.js
│       ├── index.css
│       ├── index.js
│       ├── pages/
│       │   ├── AIAssistantPage.css
│       │   ├── AIAssistantPage.js
│       │   ├── DashboardPage.css
│       │   ├── DashboardPage.js
│       │   ├── LoginPage.css
│       │   ├── LoginPage.js
│       │   ├── ModulesPage.css
│       │   ├── ModulesPage.js
│       │   ├── ProfilePage.css
│       │   └── ProfilePage.js
│       └── styles
├── js/
│   ├── ai-tutor.js
│   ├── auth.js
│   ├── dashboard.js
│   ├── main.js
│   └── modules.js
├── legacy/
│   ├── ai-tutor.html
│   ├── dashboard.html
│   ├── index.html
│   ├── login.html
│   └── modules.html
├── Dockerfile
├── README.md

## 🎮 Usage Guide

### Navigation

- **Sidebar**: Access different sections (Dashboard, Modules, CTF Labs, AI Tutor, Profile)
- **Top Bar**: View notifications, user menu, and section-specific controls
- **Responsive**: Mobile-friendly navigation with hamburger menu

### Learning Flow

1. **Start**: Visit the landing page and click "Start Learning"
2. **Register**: Create an account or login with OAuth
3. **Dashboard**: View your progress and recommended content
4. **Modules**: Browse learning modules by difficulty and category
5. **AI Tutor**: Get personalized help and explanations
6. **Practice**: Complete challenges and earn XP

### AI Tutor Features

- **Ask Questions**: Type any cybersecurity-related question
- **Quick Actions**: Use predefined prompts for common topics
- **Voice Input**: Click the microphone button for voice commands
- **Code Examples**: View syntax-highlighted code with copy functionality
- **Export Chat**: Download conversation history

## 🛠️ Customization

### Adding New Modules

1. Edit `modules.html` to add new module cards
2. Update `css/modules.css` for styling
3. Modify `js/modules.js` for interactions

### Customizing Colors

1. Edit CSS variables in `css/style.css`
2. Update the `:root` selector with your color scheme
3. All components will automatically use the new colors

### Adding Animations

1. Define new animations in `css/animations.css`
2. Use GSAP for complex animations in JavaScript files
3. Apply classes or call animation functions as needed

## 🔧 Development

### Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

### Performance

- Optimized animations with GSAP
- Efficient DOM manipulation
- Lazy loading for better performance
- Responsive images and assets

### Accessibility

- Semantic HTML structure
- ARIA labels and roles
- Keyboard navigation support
- High contrast color scheme
- Screen reader compatibility

## 🎯 Future Enhancements

### Planned Features

- **Real-time Collaboration**: Multi-user CTF challenges
- **Advanced AI**: Integration with GPT-4 or similar
- **Progress Analytics**: Detailed learning analytics
- **Mobile App**: React Native or Flutter app
- **Backend Integration**: User authentication and data persistence
- **Video Lessons**: Embedded video content
- **Achievement System**: More badges and rewards
- **Community Features**: Forums and discussion boards

### Technical Improvements

- **PWA Support**: Progressive Web App capabilities
- **Offline Mode**: Service worker for offline access
- **Performance**: Code splitting and lazy loading
- **Testing**: Unit and integration tests
- **CI/CD**: Automated deployment pipeline

## 🤝 Contributing

We welcome contributions from the community!

- See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/contributing.md](docs/contributing.md) for guidelines.
- Please follow the code of conduct in [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
- Open issues and pull requests to help improve CipherQuest.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Fonts**: Google Fonts (Orbitron, Fira Code, Montserrat)
- **Icons**: Font Awesome
- **Animations**: GSAP (GreenSock)
- **Design Inspiration**: Cyberpunk aesthetics and modern web design trends

## 📞 Support

- **Issues**: Report bugs and feature requests via GitHub Issues
- **Discussions**: Join community discussions on GitHub Discussions
- **Email**: Contact the development team for support
  
*Hack. Learn. Level Up.*
