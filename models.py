# This file is kept for compatibility with Flask patterns
# but we're using Firebase Firestore instead of SQLAlchemy

# Firestore Collections Structure:
# 
# threads/
#   - id (auto-generated)
#   - title: string
#   - content: string
#   - category: string
#   - author_uid: string
#   - author_name: string
#   - created_at: timestamp
#   - updated_at: timestamp
#   - upvotes: number
#   - downvotes: number
#   - reply_count: number
#
# replies/
#   - id (auto-generated)
#   - thread_id: string
#   - content: string
#   - author_uid: string
#   - author_name: string
#   - created_at: timestamp
#   - upvotes: number
#   - downvotes: number
#
# votes/
#   - id (auto-generated)
#   - item_id: string (thread or reply ID)
#   - item_type: string ('thread' or 'reply')
#   - vote_type: string ('upvote' or 'downvote')
#   - user_uid: string
#   - created_at: timestamp

# Sample data structure for reference:
SAMPLE_THREAD = {
    'title': 'Welcome to RetroForum!',
    'content': 'This is the first thread on our awesome retro forum.',
    'category': 'general',
    'author_uid': 'user123',
    'author_name': 'WebMaster',
    'created_at': None,  # Will be set to datetime.utcnow()
    'updated_at': None,  # Will be set to datetime.utcnow()
    'upvotes': 0,
    'downvotes': 0,
    'reply_count': 0
}

SAMPLE_REPLY = {
    'thread_id': 'thread123',
    'content': 'Great forum! Looking forward to more discussions.',
    'author_uid': 'user456',
    'author_name': 'ForumUser',
    'created_at': None,  # Will be set to datetime.utcnow()
    'upvotes': 0,
    'downvotes': 0
}

SAMPLE_VOTE = {
    'item_id': 'thread123',
    'item_type': 'thread',
    'vote_type': 'upvote',
    'user_uid': 'user789',
    'created_at': None  # Will be set to datetime.utcnow()
}
