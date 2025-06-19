"""
Basic tests for the Expense Tracker application
"""
import pytest
from app import create_app, db
from app.models.user import User
from app.models.expense import Category, Expense


@pytest.fixture
def app():
    """Create and configure a test app"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()


@pytest.fixture
def test_user(app):
    """Create a test user"""
    user = User(
        username='testuser',
        email='test@example.com',
        password='TestPass123',
        first_name='Test',
        last_name='User'
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def test_category(app):
    """Create a test category"""
    category = Category(
        name='Test Category',
        description='Test description',
        color='#007bff'
    )
    db.session.add(category)
    db.session.commit()
    return category


def test_app_creation(app):
    """Test that the app is created successfully"""
    assert app is not None


def test_user_creation(test_user):
    """Test user creation"""
    assert test_user.username == 'testuser'
    assert test_user.email == 'test@example.com'
    assert test_user.check_password('TestPass123')
    assert test_user.full_name == 'Test User'


def test_category_creation(test_category):
    """Test category creation"""
    assert test_category.name == 'Test Category'
    assert test_category.color == '#007bff'


def test_expense_creation(app, test_user, test_category):
    """Test expense creation"""
    expense = Expense(
        title='Test Expense',
        description='Test description',
        amount=25.50,
        user_id=test_user.id,
        category_id=test_category.id
    )
    db.session.add(expense)
    db.session.commit()
    
    assert expense.title == 'Test Expense'
    assert float(expense.amount) == 25.50
    assert expense.user_id == test_user.id
    assert expense.category_id == test_category.id


def test_home_page(client):
    """Test home page loads"""
    response = client.get('/')
    assert response.status_code == 200


def test_login_page(client):
    """Test login page loads"""
    response = client.get('/auth/login')
    assert response.status_code == 200


def test_register_page(client):
    """Test register page loads"""
    response = client.get('/auth/register')
    assert response.status_code == 200


def test_user_registration(client):
    """Test user registration via API"""
    response = client.post('/auth/register', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'NewPass123',
        'confirm_password': 'NewPass123',
        'first_name': 'New',
        'last_name': 'User'
    })
    
    # Should redirect or return success
    assert response.status_code in [200, 302]


def test_api_categories_unauthorized(client):
    """Test that API requires authentication"""
    response = client.get('/api/categories')
    assert response.status_code == 302  # Redirect to login


if __name__ == '__main__':
    pytest.main([__file__])
