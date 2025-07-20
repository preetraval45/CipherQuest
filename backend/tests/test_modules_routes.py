import pytest
import json
from unittest.mock import patch
from backend.app import create_app
from backend.models.user import User, db
from backend.models.module import Module
from backend.models.progress import UserProgress

@pytest.fixture
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def db_session(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture
def auth_headers(client, db_session):
    """Create a user and return auth headers"""
    # Register user
    user_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'TestPass123!'
    }
    client.post('/api/auth/register', json=user_data)
    
    # Login to get token
    login_data = {
        'username': 'testuser',
        'password': 'TestPass123!'
    }
    response = client.post('/api/auth/login', json=login_data)
    token = response.get_json()['access_token']
    
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def sample_modules(db_session):
    """Create sample modules for testing"""
    modules = [
        Module(
            title='Cryptography Basics',
            description='Learn encryption fundamentals',
            difficulty='beginner',
            category='Cryptography',
            order=1,
            is_active=True
        ),
        Module(
            title='Network Security',
            description='Network vulnerabilities and protection',
            difficulty='intermediate',
            category='Networking',
            order=2,
            is_active=True
        ),
        Module(
            title='Web Security',
            description='Web application security',
            difficulty='advanced',
            category='Web Security',
            order=3,
            is_active=True
        )
    ]
    
    for module in modules:
        db.session.add(module)
    db.session.commit()
    return modules

class TestModulesRoutes:
    def test_get_modules_success(self, client, auth_headers, sample_modules):
        """Test successful retrieval of modules"""
        response = client.get('/api/modules', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'modules' in data
        assert len(data['modules']) == 3

    def test_get_modules_unauthorized(self, client):
        """Test getting modules without authentication"""
        response = client.get('/api/modules')
        assert response.status_code == 401

    def test_get_modules_with_filtering(self, client, auth_headers, sample_modules):
        """Test filtering modules by difficulty"""
        response = client.get('/api/modules?difficulty=beginner', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['modules']) == 1
        assert data['modules'][0]['difficulty'] == 'beginner'

    def test_get_modules_with_category_filter(self, client, auth_headers, sample_modules):
        """Test filtering modules by category"""
        response = client.get('/api/modules?category=Cryptography', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['modules']) == 1
        assert data['modules'][0]['category'] == 'Cryptography'

    def test_get_modules_with_pagination(self, client, auth_headers, sample_modules):
        """Test pagination of modules"""
        response = client.get('/api/modules?limit=2&offset=0', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['modules']) == 2
        assert data['limit'] == 2
        assert data['offset'] == 0

    def test_get_modules_search(self, client, auth_headers, sample_modules):
        """Test searching modules"""
        response = client.get('/api/modules?search=cryptography', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['modules']) == 1
        assert 'cryptography' in data['modules'][0]['title'].lower()

    def test_get_module_by_id_success(self, client, auth_headers, sample_modules):
        """Test getting a specific module by ID"""
        module_id = sample_modules[0].id
        response = client.get(f'/api/modules/{module_id}', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data['module']['id'] == module_id
        assert data['module']['title'] == 'Cryptography Basics'

    def test_get_module_by_id_not_found(self, client, auth_headers):
        """Test getting a non-existent module"""
        response = client.get('/api/modules/999', headers=auth_headers)
        assert response.status_code == 404

    def test_get_module_progress(self, client, auth_headers, sample_modules, db_session):
        """Test getting user progress for a module"""
        module_id = sample_modules[0].id
        
        # Create progress record
        user = User.query.filter_by(username='testuser').first()
        progress = UserProgress(
            user_id=user.id,
            module_id=module_id,
            progress=50,
            completed=False
        )
        db.session.add(progress)
        db.session.commit()
        
        response = client.get(f'/api/modules/{module_id}/progress', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'progress' in data
        assert data['progress']['progress'] == 50

    def test_update_module_progress(self, client, auth_headers, sample_modules):
        """Test updating user progress for a module"""
        module_id = sample_modules[0].id
        progress_data = {'progress': 75}
        
        response = client.put(f'/api/modules/{module_id}/progress', 
                            json=progress_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'progress' in data
        assert data['progress']['progress'] == 75

    def test_complete_module(self, client, auth_headers, sample_modules):
        """Test marking a module as completed"""
        module_id = sample_modules[0].id
        
        response = client.post(f'/api/modules/{module_id}/complete', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        assert 'message' in data
        assert 'completed' in data

    def test_get_modules_with_inactive_filter(self, client, auth_headers, sample_modules, db_session):
        """Test that inactive modules are not returned by default"""
        # Create an inactive module
        inactive_module = Module(
            title='Inactive Module',
            description='This module is inactive',
            difficulty='beginner',
            category='Test',
            order=4,
            is_active=False
        )
        db.session.add(inactive_module)
        db.session.commit()
        
        response = client.get('/api/modules', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        # Should only return active modules
        assert len(data['modules']) == 3
        assert all(module['is_active'] for module in data['modules'])

    def test_get_modules_sorted_by_order(self, client, auth_headers, sample_modules):
        """Test that modules are returned in correct order"""
        response = client.get('/api/modules', headers=auth_headers)
        assert response.status_code == 200
        data = response.get_json()
        
        # Check that modules are sorted by order
        orders = [module['order'] for module in data['modules']]
        assert orders == sorted(orders) 