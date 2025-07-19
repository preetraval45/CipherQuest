# CipherQuest Frontend

A modern React-based frontend for the CipherQuest cybersecurity learning platform.

## 🚀 Features

- **Modern React Architecture**: Built with React 18 and functional components
- **Responsive Design**: Mobile-first approach with cyberpunk styling
- **Protected Routes**: Authentication-based route protection
- **Real-time Chat**: AI-powered cybersecurity tutoring interface
- **Interactive Dashboard**: User progress tracking and statistics
- **Module Management**: Learning module browsing and filtering
- **Profile Management**: User profile and achievement tracking

## 📁 Project Structure

```text
frontend/
├── public/
│   ├── index.html          # Main HTML template
│   └── manifest.json       # PWA manifest
├── src/
│   ├── components/
│   │   ├── auth/
│   │   │   └── ProtectedRoute.js
│   │   └── layout/
│   │       ├── Layout.js
│   │       └── Layout.css
│   ├── pages/
│   │   ├── LoginPage.js
│   │   ├── LoginPage.css
│   │   ├── DashboardPage.js
│   │   ├── DashboardPage.css
│   │   ├── ModulesPage.js
│   │   ├── ModulesPage.css
│   │   ├── AIAssistantPage.js
│   │   ├── AIAssistantPage.css
│   │   ├── ProfilePage.js
│   │   └── ProfilePage.css
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## 🛠️ Setup Instructions

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn package manager

### Installation

1. **Navigate to the frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Start the development server**
   ```bash
   npm start
   # or
   yarn start
   ```

4. **Open your browser**
   - Navigate to `http://localhost:3000`
   - The application will automatically reload when you make changes

### Available Scripts

- `npm start` - Starts the development server
- `npm build` - Builds the app for production
- `npm test` - Runs the test suite
- `npm eject` - Ejects from Create React App (irreversible)

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

### Components

#### Layout Component
- Responsive sidebar navigation
- Mobile-friendly hamburger menu
- Glassmorphism effects
- Smooth transitions

#### Authentication
- Login/Signup forms
- Form validation
- Protected route system
- Social login options

#### Dashboard
- User statistics cards
- Recent activity feed
- Leaderboard
- Recommended content

#### Modules
- Grid and list view modes
- Search and filtering
- Progress tracking
- Difficulty indicators

#### AI Assistant
- Real-time chat interface
- Quick action buttons
- Voice input support
- Code syntax highlighting

#### Profile
- User information display
- Achievement tracking
- Statistics visualization
- Settings management

## 🔧 Development

### Adding New Pages

1. Create a new component in `src/pages/`
2. Add corresponding CSS file
3. Import and add route in `App.js`
4. Add navigation item in `Layout.js`

### Styling Guidelines

- Use CSS variables for consistent theming
- Follow the cyberpunk design system
- Implement responsive design patterns
- Use glassmorphism effects for cards
- Add hover animations for interactivity

### State Management

Currently using React's built-in state management:
- `useState` for local component state
- `useEffect` for side effects
- Context API can be added for global state if needed

## 🚀 Deployment

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

### Environment Variables

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_AI_SERVICE_URL=http://localhost:5000
```

## 📱 Browser Support

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of the CipherQuest platform. See the main README for license information.