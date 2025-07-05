import os
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from database import db, Thread, Reply, Vote
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

with app.app_context():
    # Create tables
    db.create_all()

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
        threads = Thread.query.order_by(Thread.created_at.desc()).limit(20).all()
        thread_list = []
        
        for thread in threads:
            thread_data = thread.to_dict()
            thread_data['category_name'] = CATEGORIES.get(thread.category, 'General')
            thread_list.append(thread_data)
        
        return render_template('index.html', 
                             threads=thread_list, 
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
                         categories=CATEGORIES,
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
        threads = Thread.query.filter_by(category=category_id).order_by(Thread.created_at.desc()).all()
        thread_list = []
        
        for thread in threads:
            thread_data = thread.to_dict()
            thread_data['category_name'] = CATEGORIES.get(category_id, 'General')
            thread_list.append(thread_data)
        
        return render_template('category.html', 
                             threads=thread_list, 
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

@app.route('/thread/<int:thread_id>')
def thread(thread_id):
    """Show a specific thread with replies"""
    try:
        # Get thread
        thread = Thread.query.get_or_404(thread_id)
        thread_data = thread.to_dict()
        thread_data['category_name'] = CATEGORIES.get(thread.category, 'General')
        
        # Get replies
        replies = Reply.query.filter_by(thread_id=thread_id).order_by(Reply.created_at).all()
        reply_list = [reply.to_dict() for reply in replies]
        
        return render_template('thread.html', 
                             thread=thread_data, 
                             replies=reply_list,
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
        
        # Create thread
        thread = Thread(
            title=data['title'],
            content=data['content'],
            category=data['category'],
            author_uid=data['author_uid'],
            author_name=data['author_name']
        )
        
        db.session.add(thread)
        db.session.commit()
        
        return jsonify({'success': True, 'thread_id': thread.id})
    except Exception as e:
        logging.error(f"Error creating thread: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to create thread'}), 500

@app.route('/api/create_reply', methods=['POST'])
def api_create_reply():
    """API endpoint to create a new reply"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['thread_id', 'content', 'author_uid', 'author_name']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create reply
        reply = Reply(
            thread_id=int(data['thread_id']),
            content=data['content'],
            author_uid=data['author_uid'],
            author_name=data['author_name']
        )
        
        db.session.add(reply)
        
        # Update thread reply count
        thread = Thread.query.get(int(data['thread_id']))
        if thread:
            thread.reply_count += 1
            thread.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'success': True, 'reply_id': reply.id})
    except Exception as e:
        logging.error(f"Error creating reply: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to create reply'}), 500

@app.route('/api/vote', methods=['POST'])
def api_vote():
    """API endpoint to handle voting"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ['item_id', 'item_type', 'vote_type', 'user_uid']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        item_id = int(data['item_id'])
        item_type = data['item_type']  # 'thread' or 'reply'
        vote_type = data['vote_type']  # 'upvote' or 'downvote'
        user_uid = data['user_uid']
        
        # Check if user already voted
        existing_vote = Vote.query.filter_by(
            item_id=item_id,
            item_type=item_type,
            user_uid=user_uid
        ).first()
        
        # Remove existing vote if any
        if existing_vote:
            old_vote_type = existing_vote.vote_type
            db.session.delete(existing_vote)
            
            # Decrement old vote count
            if item_type == 'thread':
                item = Thread.query.get(item_id)
            else:
                item = Reply.query.get(item_id)
            
            if item:
                if old_vote_type == 'upvote':
                    item.upvotes = max(0, item.upvotes - 1)
                else:
                    item.downvotes = max(0, item.downvotes - 1)
        
        # Add new vote if different from existing or if no existing vote
        if not existing_vote or existing_vote.vote_type != vote_type:
            # Create new vote
            new_vote = Vote(
                item_id=item_id,
                item_type=item_type,
                vote_type=vote_type,
                user_uid=user_uid
            )
            db.session.add(new_vote)
            
            # Increment vote count
            if item_type == 'thread':
                item = Thread.query.get(item_id)
            else:
                item = Reply.query.get(item_id)
            
            if item:
                if vote_type == 'upvote':
                    item.upvotes += 1
                else:
                    item.downvotes += 1
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        logging.error(f"Error handling vote: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to process vote'}), 500

@app.route('/search')
def search():
    """Search threads and replies"""
    query = request.args.get('q', '').strip()
    if not query:
        return redirect(url_for('index'))
    
    try:
        # Simple text search in thread titles and content
        threads = Thread.query.filter(
            (Thread.title.ilike(f'%{query}%')) | 
            (Thread.content.ilike(f'%{query}%'))
        ).order_by(Thread.created_at.desc()).all()
        
        thread_list = []
        for thread in threads:
            thread_data = thread.to_dict()
            thread_data['category_name'] = CATEGORIES.get(thread.category, 'General')
            thread_list.append(thread_data)
        
        return render_template('index.html', 
                             threads=thread_list, 
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
