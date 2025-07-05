// Firebase Authentication Module

let currentUser = null;
window.currentUser = null;

// Initialize auth state listener
document.addEventListener('DOMContentLoaded', function() {
    if (window.auth) {
        initializeAuthListener();
    } else {
        // Wait for Firebase to be initialized
        setTimeout(initializeAuthListener, 1000);
    }
});

function initializeAuthListener() {
    if (!window.auth) {
        console.error('Firebase auth not initialized');
        return;
    }

    // Listen for auth state changes
    window.auth.onAuthStateChanged(function(user) {
        currentUser = user;
        window.currentUser = user;
        updateUIForAuthState(user);
    });
}

function updateUIForAuthState(user) {
    const loginBtn = document.getElementById('login-btn');
    const userInfo = document.getElementById('user-info');
    const userName = document.getElementById('user-name');
    const logoutBtn = document.getElementById('logout-btn');
    const newThreadBtn = document.getElementById('new-thread-btn');

    if (user) {
        // User is signed in
        if (loginBtn) loginBtn.style.display = 'none';
        if (userInfo) userInfo.style.display = 'inline';
        if (userName) userName.textContent = user.displayName || user.email || 'User';
        if (newThreadBtn) newThreadBtn.style.display = 'inline-block';
        
        // Add logout functionality
        if (logoutBtn) {
            logoutBtn.onclick = function() {
                window.auth.signOut().then(() => {
                    console.log('User signed out');
                    window.location.reload();
                }).catch((error) => {
                    console.error('Sign out error:', error);
                });
            };
        }
    } else {
        // User is signed out
        if (loginBtn) loginBtn.style.display = 'inline-block';
        if (userInfo) userInfo.style.display = 'none';
        if (newThreadBtn) {
            newThreadBtn.onclick = function(e) {
                e.preventDefault();
                alert('Please log in to create a thread.');
                window.location.href = '/login';
            };
        }
    }
}

// Utility function to check if user is authenticated
function requireAuth() {
    if (!currentUser) {
        alert('Please log in to perform this action.');
        window.location.href = '/login';
        return false;
    }
    return true;
}

// Export for use in other modules
window.requireAuth = requireAuth;
window.getCurrentUser = () => currentUser;
