# RetroForum - Nostalgic Discussion Board

## Overview

RetroForum is a Flask-based web application that recreates the nostalgic feel of 1990s internet forums. The application features a retro aesthetic with modern functionality, allowing users to create discussion threads, reply to posts, and vote on content. The system uses Firebase for authentication and data storage, providing a scalable backend infrastructure.

## System Architecture

### Frontend Architecture
- **Technology Stack**: HTML5, CSS3, JavaScript (Vanilla), Bootstrap 5
- **Design Philosophy**: Retro 1990s aesthetic with modern responsive design
- **UI Components**: Template-based rendering using Jinja2 with Flask
- **Styling Approach**: Custom CSS with retro color schemes and typography
- **Interactive Features**: Client-side JavaScript for voting, authentication, and dynamic content

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Authentication**: Firebase Authentication with Google OAuth integration
- **Data Storage**: Google Firestore (NoSQL document database)
- **Session Management**: Flask sessions with configurable secret key
- **API Design**: RESTful endpoints for voting and content management

### Data Storage Solutions
- **Primary Database**: Google Firestore
- **Collections Structure**:
  - `threads/` - Discussion threads with metadata
  - `replies/` - Thread replies and responses
  - `votes/` - User voting records for threads and replies
- **Development Fallback**: Mock Firestore client for offline development

## Key Components

### Core Application (`app.py`)
- Main Flask application with route handlers
- Forum categories management (General, Tech, Gaming, Music, Movies, Random)
- Thread creation and display functionality
- Integration with Firebase authentication and Firestore

### Firebase Integration (`firebase_config.py`)
- Firebase service initialization
- Firestore client management
- Mock client implementation for development environments
- Error handling and logging for Firebase operations

### Data Models (`models.py`)
- Document structure definitions for Firestore collections
- Sample data templates for development
- Schema documentation for threads, replies, and votes

### Frontend Templates (`templates/`)
- **Base Template**: Common layout with retro styling and navigation
- **Index Page**: Homepage with thread listings and search functionality
- **Thread View**: Individual thread display with replies
- **Authentication**: Login page with Google OAuth integration
- **Thread Creation**: Form for creating new discussion threads
- **Category Views**: Category-specific thread listings

### Static Assets (`static/`)
- **CSS**: Retro styling with 1990s-inspired design elements
- **JavaScript Modules**:
  - Firebase authentication handling
  - Voting system implementation
  - General forum functionality and navigation

## Data Flow

### Authentication Flow
1. User clicks login button
2. Firebase Auth redirects to Google OAuth
3. User authenticates with Google
4. Firebase returns user token and profile
5. Frontend updates UI state and stores user session
6. Protected actions become available

### Thread Creation Flow
1. Authenticated user submits thread form
2. Frontend validates input data
3. Thread data sent to Flask backend
4. Backend creates Firestore document
5. User redirected to new thread view
6. Thread appears in category and main listings

### Voting System Flow
1. User clicks vote button (upvote/downvote)
2. JavaScript validates authentication state
3. Vote data sent to `/api/vote` endpoint
4. Backend checks for existing votes and updates counts
5. Firestore documents updated atomically
6. Frontend updates vote display in real-time

## External Dependencies

### Firebase Services
- **Firebase Authentication**: Google OAuth provider for user management
- **Google Firestore**: NoSQL database for all application data
- **Configuration**: Environment variables for API keys and project settings

### Frontend Libraries
- **Bootstrap 5**: Responsive CSS framework with component library
- **Font Awesome**: Icon library for UI elements
- **Google Fonts**: Custom typography (Courier Prime, Press Start 2P)

### Python Packages
- **Flask**: Web framework for backend application
- **google-cloud-firestore**: Official Firestore client library
- **Standard Libraries**: os, logging, datetime, uuid

## Deployment Strategy

### Environment Configuration
- **Development**: Mock Firestore client when Firebase unavailable
- **Production**: Full Firebase integration with service account credentials
- **Session Security**: Configurable secret key via environment variables

### Required Environment Variables
- `FIREBASE_API_KEY`: Firebase project API key
- `FIREBASE_PROJECT_ID`: Firebase project identifier
- `FIREBASE_APP_ID`: Firebase application identifier
- `SESSION_SECRET`: Flask session encryption key

### Hosting Considerations
- **Web Server**: Flask development server (development) or WSGI server (production)
- **Static Files**: Served through Flask or CDN in production
- **Database**: Firebase Firestore (globally distributed)
- **Authentication**: Firebase Auth (managed service)

## Changelog

```
Changelog:
- July 04, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```