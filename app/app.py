# Basic Flask app skeleton for user registration and login

from flask import Flask, request, jsonify, abort
from models import users, sessions, User, Session, hash_password, posts, Post, Reply
import uuid
import time

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    if username in users:
        return jsonify({'error': 'Username already exists'}), 400
    users[username] = User(username=username, password_hash=hash_password(password))
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    user = users.get(username)
    if not user or user.password_hash != hash_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    session_id = str(uuid.uuid4())
    sessions[session_id] = Session(session_id=session_id, username=username)
    return jsonify({'session_id': session_id})


# Profile management endpoints

def get_user_from_session():
    session_id = request.headers.get('Authorization')
    if not session_id or session_id not in sessions:
        abort(401, description='Invalid or missing session')
    return users[sessions[session_id].username]

@app.route('/profile', methods=['GET'])
def get_profile():
    user = get_user_from_session()
    return jsonify({
        'username': user.username,
        'display_name': user.display_name,
        'bio': user.bio
    })

@app.route('/profile/update', methods=['POST'])
def update_profile():
    user = get_user_from_session()
    data = request.json
    display_name = data.get('display_name')
    bio = data.get('bio')
    if display_name is not None:
        user.display_name = display_name
    if bio is not None:
        user.bio = bio
    return jsonify({'message': 'Profile updated successfully'})

# --- Posting System Endpoints ---

def get_post_or_404(post_id):
    post = posts.get(post_id)
    if not post:
        abort(404, description='Post not found')
    return post

@app.route('/post', methods=['POST'])
def create_post():
    user = get_user_from_session()
    data = request.json
    content = data.get('content')
    if not content or not content.strip():
        return jsonify({'error': 'Content required'}), 400
    post_id = str(uuid.uuid4())
    post = Post(post_id=post_id, author=user.username, content=content.strip())
    posts[post_id] = post
    return jsonify({'message': 'Post created', 'post_id': post_id})

@app.route('/post/edit', methods=['POST'])
def edit_post():
    user = get_user_from_session()
    data = request.json
    post_id = data.get('post_id')
    content = data.get('content')
    if not post_id or not content:
        return jsonify({'error': 'post_id and content required'}), 400
    post = get_post_or_404(post_id)
    if post.author != user.username:
        return jsonify({'error': 'Unauthorized'}), 403
    post.content = content.strip()
    post.updated_at = time.time()
    return jsonify({'message': 'Post updated'})

@app.route('/post/delete', methods=['POST'])
def delete_post():
    user = get_user_from_session()
    data = request.json
    post_id = data.get('post_id')
    if not post_id:
        return jsonify({'error': 'post_id required'}), 400
    post = get_post_or_404(post_id)
    if post.author != user.username:
        return jsonify({'error': 'Unauthorized'}), 403
    del posts[post_id]
    return jsonify({'message': 'Post deleted'})

@app.route('/posts', methods=['GET'])
def list_posts():
    # Optionally filter by author
    author = request.args.get('author')
    result = []
    for post in posts.values():
        if author and post.author != author:
            continue
        result.append({
            'post_id': post.post_id,
            'author': post.author,
            'content': post.content,
            'created_at': post.created_at,
            'updated_at': post.updated_at
        })
    return jsonify({'posts': result})

# --- Feed Endpoint ---

@app.route('/feed', methods=['GET'])
def feed():
    try:
        offset = int(request.args.get('offset', 0))
        limit = int(request.args.get('limit', 20))
    except ValueError:
        return jsonify({'error': 'offset and limit must be integers'}), 400
    if offset < 0 or limit <= 0:
        return jsonify({'error': 'offset must be >= 0 and limit must be > 0'}), 400

    all_posts = sorted(posts.values(), key=lambda p: p.created_at, reverse=True)
    total_count = len(all_posts)
    page = all_posts[offset:offset + limit]

    result = []
    for post in page:
        result.append({
            'post_id': post.post_id,
            'author': post.author,
            'content': post.content,
            'created_at': post.created_at,
            'updated_at': post.updated_at,
            'like_count': len(post.likes),
            'reply_count': len(post.replies),
            'replies': [{'reply_id': r.reply_id, 'author': r.author,
                         'content': r.content, 'created_at': r.created_at}
                        for r in post.replies]
        })
    return jsonify({'posts': result, 'total_count': total_count,
                    'offset': offset, 'limit': limit})

# --- Like Endpoint ---

@app.route('/post/like', methods=['POST'])
def like_post():
    user = get_user_from_session()
    data = request.json
    post_id = data.get('post_id')
    if not post_id:
        return jsonify({'error': 'post_id required'}), 400
    post = get_post_or_404(post_id)
    if post.author == user.username:
        return jsonify({'error': 'Cannot like your own post'}), 400
    if user.username in post.likes:
        return jsonify({'error': 'Already liked'}), 400
    post.likes.add(user.username)
    return jsonify({'message': 'Post liked', 'like_count': len(post.likes)})

# --- Reply Endpoint ---

@app.route('/post/reply', methods=['POST'])
def reply_to_post():
    user = get_user_from_session()
    data = request.json
    post_id = data.get('post_id')
    content = data.get('content')
    if not post_id or not content or not content.strip():
        return jsonify({'error': 'post_id and content required'}), 400
    post = get_post_or_404(post_id)
    reply_id = str(uuid.uuid4())
    reply = Reply(reply_id=reply_id, author=user.username, content=content.strip())
    post.replies.append(reply)
    return jsonify({'message': 'Reply added', 'reply': {
        'reply_id': reply.reply_id, 'author': reply.author,
        'content': reply.content, 'created_at': reply.created_at
    }})

# --- Public User Profile ---

@app.route('/user/<username>', methods=['GET'])
def user_profile(username):
    user = users.get(username)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    user_posts = sorted(
        [p for p in posts.values() if p.author == username],
        key=lambda p: p.created_at, reverse=True
    )
    return jsonify({
        'username': user.username,
        'bio': user.bio,
        'posts': [{
            'post_id': p.post_id,
            'content': p.content,
            'created_at': p.created_at,
            'updated_at': p.updated_at,
            'like_count': len(p.likes),
            'reply_count': len(p.replies)
        } for p in user_posts]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
