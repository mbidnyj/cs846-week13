import requests

BASE_URL = 'http://127.0.0.1:5001'

# Register a user
def test_register():
    r = requests.post(f'{BASE_URL}/register', json={'username': 'alice', 'password': 'password123'})
    print('Register:', r.json())

def test_login():
    r = requests.post(f'{BASE_URL}/login', json={'username': 'alice', 'password': 'password123'})
    print('Login:', r.json())
    return r.json().get('session_id')

def test_profile(session_id):
    r = requests.get(f'{BASE_URL}/profile', headers={'Authorization': session_id})
    print('Get profile:', r.json())

def test_update_profile(session_id):
    r = requests.post(f'{BASE_URL}/profile/update', json={'display_name': 'Alice', 'bio': 'Hello!'}, headers={'Authorization': session_id})
    print('Update profile:', r.json())
    r2 = requests.get(f'{BASE_URL}/profile', headers={'Authorization': session_id})
    print('Profile after update:', r2.json())

if __name__ == '__main__':
    test_register()
    session_id = test_login()
    if session_id:
        test_profile(session_id)
        test_update_profile(session_id)
