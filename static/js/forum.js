// General Forum JavaScript Functions

document.addEventListener('DOMContentLoaded', function() {
    initializeForumFeatures();
});

function initializeForumFeatures() {
    // Initialize thread row click handling
    initializeThreadNavigation();
    
    // Initialize retro effects
    initializeRetroEffects();
    
    // Initialize form enhancements
    initializeFormEnhancements();
    
    // Initialize keyboard shortcuts
    initializeKeyboardShortcuts();
}

function initializeThreadNavigation() {
    // Make thread rows clickable
    const threadRows = document.querySelectorAll('.thread-row');
    
    threadRows.forEach(row => {
        row.addEventListener('click', function(e) {
            // Don't navigate if clicking on vote buttons or links
            if (e.target.closest('.vote-btn') || e.target.closest('a')) {
                return;
            }
            
            const threadLink = this.querySelector('.thread-link');
            if (threadLink) {
                window.location.href = threadLink.href;
            }
        });
        
        // Add hover effect
        row.style.cursor = 'pointer';
    });
}

function initializeRetroEffects() {
    // Add typing effect to new content
    const typingElements = document.querySelectorAll('.typing-effect');
    
    typingElements.forEach(element => {
        addTypingEffect(element);
    });
    
    // Add retro computer sounds (optional)
    addRetroSounds();
}

function addTypingEffect(element) {
    const text = element.textContent;
    element.textContent = '';
    element.style.borderRight = '2px solid var(--retro-accent)';
    
    let i = 0;
    const typeInterval = setInterval(() => {
        element.textContent += text.charAt(i);
        i++;
        
        if (i >= text.length) {
            clearInterval(typeInterval);
            // Remove cursor after typing
            setTimeout(() => {
                element.style.borderRight = 'none';
            }, 1000);
        }
    }, 50);
}

function addRetroSounds() {
    // Add subtle click sounds to buttons (using Web Audio API)
    const buttons = document.querySelectorAll('.retro-button, .vote-btn');
    
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            playClickSound();
        });
    });
}

function playClickSound() {
    try {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();
        
        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);
        
        oscillator.frequency.setValueAtTime(1000, audioContext.currentTime);
        oscillator.frequency.setValueAtTime(800, audioContext.currentTime + 0.1);
        
        gainNode.gain.setValueAtTime(0.1, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
        
        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.1);
    } catch (e) {
        // Audio context not supported, silently fail
    }
}

function initializeFormEnhancements() {
    // Add character counters to textareas
    const textareas = document.querySelectorAll('.retro-textarea');
    
    textareas.forEach(textarea => {
        addCharacterCounter(textarea);
    });
    
    // Add auto-resize to textareas
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            autoResizeTextarea(this);
        });
    });
    
    // Add form validation styling
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        addFormValidation(form);
    });
}

function addCharacterCounter(textarea) {
    const maxLength = textarea.getAttribute('maxlength');
    if (!maxLength) return;
    
    const counter = document.createElement('div');
    counter.className = 'character-counter';
    counter.style.cssText = `
        font-size: 10px;
        color: var(--retro-button-shadow);
        text-align: right;
        margin-top: 2px;
    `;
    
    textarea.parentNode.appendChild(counter);
    
    function updateCounter() {
        const remaining = maxLength - textarea.value.length;
        counter.textContent = `${remaining} characters remaining`;
        
        if (remaining < 20) {
            counter.style.color = 'var(--retro-error)';
        } else if (remaining < 50) {
            counter.style.color = 'var(--retro-warning)';
        } else {
            counter.style.color = 'var(--retro-button-shadow)';
        }
    }
    
    textarea.addEventListener('input', updateCounter);
    updateCounter();
}

function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

function addFormValidation(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(this);
        });
        
        input.addEventListener('input', function() {
            // Remove error styling when user starts typing
            this.classList.remove('field-error');
        });
    });
    
    form.addEventListener('submit', function(e) {
        let isValid = true;
        
        inputs.forEach(input => {
            if (!validateField(input)) {
                isValid = false;
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            showFormError('Please fill in all required fields correctly.');
        }
    });
}

function validateField(field) {
    const value = field.value.trim();
    const isValid = value.length > 0;
    
    if (!isValid) {
        field.classList.add('field-error');
    } else {
        field.classList.remove('field-error');
    }
    
    return isValid;
}

function showFormError(message) {
    const existingError = document.querySelector('.form-error-message');
    if (existingError) {
        existingError.remove();
    }
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'form-error-message retro-alert alert-danger';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
    
    const form = document.querySelector('form');
    if (form) {
        form.parentNode.insertBefore(errorDiv, form);
        
        // Remove error after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.remove();
            }
        }, 5000);
    }
}

function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit forms
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeElement = document.activeElement;
            if (activeElement.tagName === 'TEXTAREA') {
                const form = activeElement.closest('form');
                if (form) {
                    const submitBtn = form.querySelector('button[type="submit"]');
                    if (submitBtn) {
                        submitBtn.click();
                    }
                }
            }
        }
        
        // Escape key to cancel forms
        if (e.key === 'Escape') {
            const cancelBtn = document.querySelector('#cancel-reply, .cancel-btn');
            if (cancelBtn) {
                cancelBtn.click();
            }
        }
    });
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `retro-notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'exclamation-triangle' : 'info'}"></i>
        ${message}
    `;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--retro-${type === 'success' ? 'success' : type === 'error' ? 'error' : 'link'});
        color: white;
        padding: 10px 15px;
        border: 2px solid var(--retro-border);
        border-radius: 4px;
        z-index: 1000;
        font-size: 12px;
        font-weight: bold;
        max-width: 300px;
        animation: slideInRight 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 3000);
}

// Scroll to top functionality
function addScrollToTop() {
    const scrollBtn = document.createElement('button');
    scrollBtn.className = 'scroll-to-top retro-button';
    scrollBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        display: none;
        padding: 8px 10px;
    `;
    
    document.body.appendChild(scrollBtn);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollBtn.style.display = 'block';
        } else {
            scrollBtn.style.display = 'none';
        }
    });
    
    scrollBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Initialize scroll to top
addScrollToTop();

// Add additional CSS for new features
const additionalStyles = document.createElement('style');
additionalStyles.textContent = `
    .field-error {
        border-color: var(--retro-error) !important;
        background: #ffe6e6 !important;
    }
    
    .character-counter {
        font-family: monospace;
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .scroll-to-top {
        transition: opacity 0.3s ease;
    }
    
    .thread-row:hover {
        background: var(--retro-highlight) !important;
    }
`;
document.head.appendChild(additionalStyles);

// Export utility functions
window.showNotification = showNotification;
window.playClickSound = playClickSound;
