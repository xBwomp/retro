import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from firebase_config import initialize_firebase, get_firestore_client
from datetime import datetime
import uuid

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Initialize Firebase
initialize_firebase()
db = get_firestore_client()

# Categories for the forum
CATEGORIES = {
    'general': 'General Discussion',
    'tech': 'Technology',
    'gaming': 'Gaming',
    'music': 'Music',
    'movies': 'Movies & TV',
    'random': 'Random Thoughts'
}

@app.route('/')
def index():
    """Main forum page showing recent threads"""
    try:
        # Get recent threads from all categories
        threads_ref = db.collection('threads').order_by('created_at', direction='DESCENDING').limit(20)
        threads = []
        
        for doc in threads_ref.stream():
            thread_data = doc.to_dict()
            thread_data['id'] = doc.id
            thread_data['category_name'] = CATEGORIES.get(thread_data.get('category', 'general'), 'General')
            threads.append(thread_data)
        
        return render_template('index.html', 
                             threads=threads, 
                             categories=CATEGORIES,
                             firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                             firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                             firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))
    except Exception as e:
        logging.error(f"Error loading index: {e}")
        return render_template('index.html', 
                             threads=[], 
                             categories=CATEGORIES,
                             firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                             firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                             firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))

@app.route('/login')
def login():
    """Login page"""
    return render_template('login.html',
                         firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                         firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                         firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))

@app.route('/category/<category_id>')
def category(category_id):
    """Show threads in a specific category"""
    if category_id not in CATEGORIES:
        flash('Category not found!', 'error')
        return redirect(url_for('index'))
    
    try:
        threads_ref = db.collection('threads').where('category', '==', category_id).order_by('created_at', direction='DESCENDING')
        threads = []
        
        for doc in threads_ref.stream():
            thread_data = doc.to_dict()
            thread_data['id'] = doc.id
            thread_data['category_name'] = CATEGORIES.get(category_id, 'General')
            threads.append(thread_data)
        
        return render_template('category.html', 
                             threads=threads, 
                             category_id=category_id,
                             category_name=CATEGORIES[category_id],
                             categories=CATEGORIES,
                             firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                             firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                             firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))
    except Exception as e:
        logging.error(f"Error loading category {category_id}: {e}")
        return render_template('category.html', 
                             threads=[], 
                             category_id=category_id,
                             category_name=CATEGORIES[category_id],
                             categories=CATEGORIES,
                             firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                             firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                             firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))

@app.route('/thread/<thread_id>')
def thread(thread_id):
    """Show a specific thread with replies"""
    try:
        # Get thread
        thread_ref = db.collection('threads').document(thread_id)
        thread_doc = thread_ref.get()
        
        if not thread_doc.exists:
            flash('Thread not found!', 'error')
            return redirect(url_for('index'))
        
        thread_data = thread_doc.to_dict()
        thread_data['id'] = thread_id
        thread_data['category_name'] = CATEGORIES.get(thread_data.get('category', 'general'), 'General')
        
        # Get replies
        replies_ref = db.collection('replies').where('thread_id', '==', thread_id).order_by('created_at')
        replies = []
        
        for doc in replies_ref.stream():
            reply_data = doc.to_dict()
            reply_data['id'] = doc.id
            replies.append(reply_data)
        
        return render_template('thread.html', 
                             thread=thread_data, 
                             replies=replies,
                             categories=CATEGORIES,
                             firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                             firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                             firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))
    except Exception as e:
        logging.error(f"Error loading thread {thread_id}: {e}")
        flash('Error loading thread!', 'error')
        return redirect(url_for('index'))

@app.route('/create_thread')
def create_thread():
    """Create a new thread form"""
    return render_template('create_thread.html', 
                         categories=CATEGORIES,
                         firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                         firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                         firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))

@app.route('/api/create_thread', methods=['POST'])
def api_create_thread():
    """API endpoint to create a new thread"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['title', 'content', 'category', 'author_uid', 'author_name']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create thread document
        thread_data = {
            'title': data['title'],
            'content': data['content'],
            'category': data['category'],
            'author_uid': data['author_uid'],
            'author_name': data['author_name'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'upvotes': 0,
            'downvotes': 0,
            'reply_count': 0
        }
        
        doc_ref = db.collection('threads').document()
        doc_ref.set(thread_data)
        
        return jsonify({'success': True, 'thread_id': doc_ref.id})
    except Exception as e:
        logging.error(f"Error creating thread: {e}")
        return jsonify({'error': 'Failed to create thread'}), 500

@app.route('/api/create_reply', methods=['POST'])
def api_create_reply():
    """API endpoint to create a new reply"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['thread_id', 'content', 'author_uid', 'author_name']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create reply document
        reply_data = {
            'thread_id': data['thread_id'],
            'content': data['content'],
            'author_uid': data['author_uid'],
            'author_name': data['author_name'],
            'created_at': datetime.utcnow(),
            'upvotes': 0,
            'downvotes': 0
        }
        
        doc_ref = db.collection('replies').document()
        doc_ref.set(reply_data)
        
        # Update thread reply count
        thread_ref = db.collection('threads').document(data['thread_id'])
        thread_ref.update({
            'reply_count': db.field_increment(1),
            'updated_at': datetime.utcnow()
        })
        
        return jsonify({'success': True, 'reply_id': doc_ref.id})
    except Exception as e:
        logging.error(f"Error creating reply: {e}")
        return jsonify({'error': 'Failed to create reply'}), 500

@app.route('/api/vote', methods=['POST'])
def api_vote():
    """API endpoint to handle voting"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['item_id', 'item_type', 'vote_type', 'user_uid']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        item_id = data['item_id']
        item_type = data['item_type']  # 'thread' or 'reply'
        vote_type = data['vote_type']  # 'upvote' or 'downvote'
        user_uid = data['user_uid']
        
        # Check if user already voted
        vote_ref = db.collection('votes').where('item_id', '==', item_id).where('user_uid', '==', user_uid)
        existing_votes = list(vote_ref.stream())
        
        # Remove existing vote if any
        for vote_doc in existing_votes:
            old_vote = vote_doc.to_dict()
            vote_doc.reference.delete()
            
            # Decrement old vote count
            collection = 'threads' if item_type == 'thread' else 'replies'
            item_ref = db.collection(collection).document(item_id)
            if old_vote['vote_type'] == 'upvote':
                item_ref.update({'upvotes': db.field_increment(-1)})
            else:
                item_ref.update({'downvotes': db.field_increment(-1)})
        
        # Add new vote if different from existing or if no existing vote
        if not existing_votes or existing_votes[0].to_dict()['vote_type'] != vote_type:
            # Create new vote
            vote_data = {
                'item_id': item_id,
                'item_type': item_type,
                'vote_type': vote_type,
                'user_uid': user_uid,
                'created_at': datetime.utcnow()
            }
            db.collection('votes').document().set(vote_data)
            
            # Increment vote count
            collection = 'threads' if item_type == 'thread' else 'replies'
            item_ref = db.collection(collection).document(item_id)
            if vote_type == 'upvote':
                item_ref.update({'upvotes': db.field_increment(1)})
            else:
                item_ref.update({'downvotes': db.field_increment(1)})
        
        return jsonify({'success': True})
    except Exception as e:
        logging.error(f"Error handling vote: {e}")
        return jsonify({'error': 'Failed to process vote'}), 500

@app.route('/search')
def search():
    """Search threads and replies"""
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('index'))
    
    try:
        # Simple text search in thread titles and content
        threads_ref = db.collection('threads')
        all_threads = threads_ref.stream()
        
        matching_threads = []
        for doc in all_threads:
            thread_data = doc.to_dict()
            if (query.lower() in thread_data.get('title', '').lower() or 
                query.lower() in thread_data.get('content', '').lower()):
                thread_data['id'] = doc.id
                thread_data['category_name'] = CATEGORIES.get(thread_data.get('category', 'general'), 'General')
                matching_threads.append(thread_data)
        
        return render_template('index.html', 
                             threads=matching_threads, 
                             categories=CATEGORIES,
                             search_query=query,
                             firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                             firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                             firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))
    except Exception as e:
        logging.error(f"Error searching: {e}")
        return render_template('index.html', 
                             threads=[], 
                             categories=CATEGORIES,
                             search_query=query,
                             firebase_api_key=os.environ.get("FIREBASE_API_KEY", ""),
                             firebase_project_id=os.environ.get("FIREBASE_PROJECT_ID", ""),
                             firebase_app_id=os.environ.get("FIREBASE_APP_ID", ""))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
