# TalkToTech Frontend

## Overview

This is the frontend application for TalkToTech, built with React and Vite. It provides an intuitive user interface for uploading audio files, viewing AI-generated summaries, and displaying interactive diagrams and code.

## Features

### 🎤 Audio Upload & Processing

- Drag-and-drop audio file upload
- Real-time upload progress
- Support for multiple audio formats (WAV, MP3, etc.)
- Audio playback and validation

### 📊 AI-Generated Content Display

- Meeting transcript display
- AI-generated summaries with structured formatting
- Interactive diagram tabs for multiple diagram types
- Real-time code generation display

### 🎨 Interactive Diagrams

- SVG diagram rendering
- Multiple diagram type support (Class, Sequence, Use Case, etc.)
- Zoom and pan functionality
- Export capabilities

### 💻 Code Generation

- Syntax-highlighted code display
- Support for multiple programming languages (Java, SQL, etc.)
- Copy-to-clipboard functionality
- Code download options

## Technology Stack

- **React 18** - Modern React with hooks and functional components
- **Vite** - Fast build tool and development server
- **CSS3** - Custom styling with modern CSS features
- **JavaScript ES6+** - Modern JavaScript features
- **PlantUML** - Diagram rendering integration

## Project Structure

```text
my-app/
├── src/
│   ├── react-components/     # Custom React components
│   │   ├── SpeechRecorder.jsx    # Audio recording component
│   │   ├── DiagramTabs.jsx       # Multi-tab diagram display
│   │   ├── PlantUMLDisplay.jsx   # Diagram rendering
│   │   ├── CodePopup.jsx         # Code display modal
│   │   ├── PDFSVGPanel.jsx       # PDF/SVG export panel
│   │   └── ...                   # Other UI components
│   ├── context/
│   │   └── RecordingContext.jsx  # Global state management
│   ├── App.jsx                   # Main application component
│   ├── main.jsx                  # Application entry point
│   └── index.css                 # Global styles
├── public/                       # Static assets
├── package.json                  # Dependencies and scripts
└── vite.config.js               # Vite configuration
```

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn package manager
- Backend server running (see components/README.md)

### Installation

```bash
cd my-app
npm install
```

### Development

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

### Building for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Component Overview

### SpeechRecorder

- Audio file upload interface
- Recording state management
- Upload progress indicators
- Error handling and validation

### DiagramTabs

- Multi-tab interface for different diagram types
- Dynamic tab generation based on AI analysis
- Tab switching and state management

### PlantUMLDisplay

- SVG diagram rendering
- Interactive diagram controls
- Responsive design for different screen sizes

### CodePopup

- Modal dialog for code display
- Syntax highlighting
- Copy and download functionality

### PDFSVGPanel

- Export functionality for diagrams
- PDF and SVG format support
- Download management

## API Integration

### Backend Communication

- RESTful API calls to Flask backend
- File upload handling
- Real-time response processing
- Error handling and user feedback

### Data Flow

```text
User Upload → Frontend → Backend API → AI Processing → Response → UI Update
```

## Styling & Design

### Design System

- Modern, clean interface design
- Responsive layout for all devices
- Consistent color scheme and typography
- Accessibility considerations

### CSS Architecture

- Component-scoped styles
- CSS custom properties for theming
- Responsive design patterns
- Modern CSS features (Grid, Flexbox)

## State Management

### RecordingContext

- Global state for recording process
- Audio file management
- Upload status tracking
- Error state handling

### Component State

- Local component state for UI interactions
- Form validation states
- Loading and error states

## Error Handling

### User Feedback

- Loading indicators during API calls
- Error messages for failed operations
- Success confirmations
- Validation feedback

### Error Recovery

- Automatic retry mechanisms
- Graceful degradation
- User-friendly error messages

## Performance Optimization

### Code Splitting

- Lazy loading of components
- Dynamic imports for heavy features
- Optimized bundle sizes

### Rendering Optimization

- React.memo for expensive components
- Efficient re-rendering strategies
- Virtual scrolling for large lists

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Development Guidelines

### Code Style

- ESLint configuration for code quality
- Consistent naming conventions
- Component documentation
- Type checking with PropTypes

### Testing

- Component unit tests
- Integration testing
- User acceptance testing
- Cross-browser testing

## Deployment

### Vercel Deployment

The application is deployed on Vercel at: [talktotech.vercel.app](https://talktotech.vercel.app/)

### Environment Variables

```bash
VITE_API_BASE_URL=http://localhost:5000  # Backend API URL
```

## Next Steps

1. ✅ Core UI components implemented
2. ✅ Backend integration complete
3. ✅ Audio upload functionality working
4. ✅ Diagram display and interaction
5. 🔄 Add user authentication
6. 🔄 Implement real-time collaboration
7. 🔄 Add offline support
8. 🔄 Enhance accessibility features
