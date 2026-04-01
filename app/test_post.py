import requests

BASE_URL = 'http://127.0.0.1:5001'

def register_and_login(username, password):
    r = requests.post(f'{BASE_URL}/register', json={'username': username, 'password': password})
    requests.post(f'{BASE_URL}/login', json={'username': username, 'password': password})
    r = requests.post(f'{BASE_URL}/login', json={'username': username, 'password': password})
    session_id = r.json().get('session_id')
    return session_id

def test_post_flow():
    username = 'alice'
    password = 'alicepass'
    session_id = register_and_login(username, password)
    headers = {'Authorization': session_id}

    # Create post
    r = requests.post(f'{BASE_URL}/post', json={'content': 'Hello world!'}, headers=headers)
    assert r.status_code == 200
    post_id = r.json()['post_id']
    print('Post created:', post_id)

    # Edit post
    r = requests.post(f'{BASE_URL}/post/edit', json={'post_id': post_id, 'content': 'Hello edited!'}, headers=headers)
    assert r.status_code == 200
    print('Post edited')

    # List posts
    r = requests.get(f'{BASE_URL}/posts')
    assert r.status_code == 200
    posts = r.json()['posts']
    assert any(p['post_id'] == post_id and p['content'] == 'Hello edited!' for p in posts)
    print('Post listed')

    # Delete post
    r = requests.post(f'{BASE_URL}/post/delete', json={'post_id': post_id}, headers=headers)
    assert r.status_code == 200
    print('Post deleted')

    # Confirm deletion
    r = requests.get(f'{BASE_URL}/posts')
    assert not any(p['post_id'] == post_id for p in r.json()['posts'])
    print('Deletion confirmed')

if __name__ == '__main__':
    test_post_flow()
