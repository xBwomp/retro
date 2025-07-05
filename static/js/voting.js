// Voting System Module

document.addEventListener('DOMContentLoaded', function() {
    initializeVoting();
});

function initializeVoting() {
    // Add event listeners to all vote buttons
    const voteButtons = document.querySelectorAll('.vote-btn');
    
    voteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const itemId = this.dataset.itemId;
            const itemType = this.dataset.itemType;
            const voteType = this.dataset.voteType;
            
            handleVote(itemId, itemType, voteType, this);
        });
    });
}

function handleVote(itemId, itemType, voteType, buttonElement) {
    // Check if user is authenticated
    if (!window.currentUser) {
        alert('Please log in to vote.');
        window.location.href = '/login';
        return;
    }
    
    // Disable button during request
    buttonElement.disabled = true;
    const originalContent = buttonElement.innerHTML;
    buttonElement.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    
    // Prepare vote data
    const voteData = {
        item_id: itemId,
        item_type: itemType,
        vote_type: voteType,
        user_uid: window.currentUser.uid
    };
    
    // Send vote to server
    fetch('/api/vote', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(voteData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update vote count in UI
            updateVoteDisplay(itemId, itemType, voteType, buttonElement);
            showVoteSuccess(voteType);
        } else {
            console.error('Vote error:', data.error);
            alert('Error processing vote: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        console.error('Vote error:', error);
        alert('Error processing vote. Please try again.');
    })
    .finally(() => {
        // Re-enable button
        buttonElement.disabled = false;
        buttonElement.innerHTML = originalContent;
    });
}

function updateVoteDisplay(itemId, itemType, voteType, clickedButton) {
    // Find the vote count span in the clicked button
    const voteCountSpan = clickedButton.querySelector('.vote-count');
    if (voteCountSpan) {
        let currentCount = parseInt(voteCountSpan.textContent) || 0;
        
        // Check if this button was already selected (would need state tracking)
        // For now, just increment the count
        voteCountSpan.textContent = currentCount + 1;
        
        // Add visual feedback
        clickedButton.classList.add('voted');
        setTimeout(() => {
            clickedButton.classList.remove('voted');
        }, 1000);
    }
}

function showVoteSuccess(voteType) {
    // Create temporary success message
    const message = document.createElement('div');
    message.className = 'vote-success-message';
    message.innerHTML = `<i class="fas fa-check"></i> ${voteType === 'upvote' ? 'Upvoted' : 'Downvoted'}!`;
    message.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--retro-success);
        color: white;
        padding: 10px 15px;
        border: 2px solid var(--retro-border);
        border-radius: 4px;
        z-index: 1000;
        font-size: 12px;
        font-weight: bold;
    `;
    
    document.body.appendChild(message);
    
    // Remove message after 2 seconds
    setTimeout(() => {
        if (message.parentNode) {
            message.parentNode.removeChild(message);
        }
    }, 2000);
}

// Add CSS for vote button feedback
const style = document.createElement('style');
style.textContent = `
    .vote-btn.voted {
        background: var(--retro-highlight) !important;
        animation: voteFlash 0.5s ease-in-out;
    }
    
    @keyframes voteFlash {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); }
    }
    
    .vote-success-message {
        animation: slideInRight 0.3s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
`;
document.head.appendChild(style);
