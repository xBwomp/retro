# RetroForum Deployment Guide

## Deploying to Your Personal Website

This guide will help you deploy RetroForum to your personal website using MySQL database.

### Prerequisites

- Python 3.8 or higher on your server
- MySQL database access
- Web server with Python support (Apache, Nginx, etc.)

### Step 1: Prepare Your Files

Copy these files to your web server:
- `app.py` - Main application
- `database.py` - Database models
- `templates/` folder - HTML templates
- `static/` folder - CSS and JavaScript files

### Step 2: Install Python Dependencies

Create a `requirements.txt` file with:
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
PyMySQL==1.1.1
cryptography==41.0.8
gunicorn==21.2.0
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### Step 3: Configure MySQL Database

1. Create a MySQL database named `retroforum`
2. Set these environment variables on your server:

```bash
export MYSQL_HOST="your-mysql-host"
export MYSQL_USER="your-mysql-username"
export MYSQL_PASSWORD="your-mysql-password"
export MYSQL_DATABASE="retroforum"
export SESSION_SECRET="your-random-secret-key"
```

### Step 4: Firebase Authentication Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or use existing one
3. Enable Authentication > Google sign-in
4. Add your domain to Authorized domains
5. Get your Firebase config and set these environment variables:

```bash
export FIREBASE_API_KEY="your-firebase-api-key"
export FIREBASE_PROJECT_ID="your-firebase-project-id"
export FIREBASE_APP_ID="your-firebase-app-id"
```

### Step 5: Deploy the Application

#### Option A: Using Gunicorn (Recommended)
```bash
gunicorn --bind 0.0.0.0:5000 main:app
```

#### Option B: Using Flask Development Server
```bash
python app.py
```

### Step 6: Configure Web Server

For Apache, add this to your virtual host:
```apache
ProxyPass /forum http://localhost:5000/
ProxyPassReverse /forum http://localhost:5000/
```

For Nginx:
```nginx
location /forum {
    proxy_pass http://localhost:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

### Database Schema

The application will automatically create these MySQL tables:
- `thread` - Discussion threads
- `reply` - Thread replies
- `vote` - User votes on threads and replies

### Environment Variables Summary

Required for production:
- `MYSQL_HOST` - Your MySQL server hostname
- `MYSQL_USER` - MySQL username
- `MYSQL_PASSWORD` - MySQL password
- `MYSQL_DATABASE` - Database name (e.g., "retroforum")
- `SESSION_SECRET` - Random secret key for sessions
- `FIREBASE_API_KEY` - Firebase API key
- `FIREBASE_PROJECT_ID` - Firebase project ID
- `FIREBASE_APP_ID` - Firebase app ID

### Testing Your Deployment

1. Visit your website at the configured path
2. Test user registration/login with Google
3. Create a test thread
4. Reply to the thread
5. Test voting functionality

### Troubleshooting

1. **Database Connection Issues**: Verify MySQL credentials and network access
2. **Firebase Auth Issues**: Check that your domain is in authorized domains list
3. **Static Files Not Loading**: Ensure web server serves static files correctly
4. **Session Issues**: Verify SESSION_SECRET is set and persistent

### Security Notes

- Always use HTTPS in production
- Keep your SESSION_SECRET secure and random
- Regularly update dependencies
- Set proper MySQL user permissions
- Configure firewall rules appropriately