import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client

def test_home_page_loads(client):
    """Test home page returns 200"""
    response = client.get('/')
    assert response.status_code == 200

def test_login_page_loads(client):
    """Test login page returns 200"""
    response = client.get('/login')
    assert response.status_code == 200

def test_register_page_loads(client):
    """Test register page returns 200"""
    response = client.get('/register')
    assert response.status_code == 200

def test_events_page_redirects_without_login(client):
    """Test events page redirects if not logged in"""
    response = client.get('/events')
    assert response.status_code == 302

def test_my_events_redirects_without_login(client):
    """Test my_events redirects if not logged in"""
    response = client.get('/my_events')
    assert response.status_code == 302

def test_admin_redirects_without_login(client):
    """Test admin page redirects if not logged in"""
    response = client.get('/admin')
    assert response.status_code == 302

def test_invalid_login(client):
    """Test login with wrong credentials"""
    response = client.post('/login', data={
        'email': 'wrong@email.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 200