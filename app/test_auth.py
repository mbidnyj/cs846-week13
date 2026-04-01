import requests

BASE_URL = 'http://127.0.0.1:5001'

def test_register():
    resp = requests.post(f'{BASE_URL}/register', json={
        'username': 'alice',
        'password': 'password123'
    })
    print('Register:', resp.status_code, resp.json())

def test_login():
    resp = requests.post(f'{BASE_URL}/login', json={
        'username': 'alice',
        'password': 'password123'
    })
    print('Login:', resp.status_code, resp.json())

if __name__ == '__main__':
    test_register()
    test_login()
