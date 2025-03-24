import pytest
from model.broker import Broker
from app import db

def test_broker_index_page(client):
    """Test that the broker index page loads correctly"""
    response = client.get('/brokers/')
    assert response.status_code == 200
    assert b'Brokers Directory' in response.data

def test_broker_form_submission(client):
    """Test that a broker can be added through the form"""
    # Test data
    test_data = {
        'name': 'Test Broker',
        'email': 'test@example.com',
        'webpage': 'http://test.com'
    }
    
    # Submit the form
    response = client.post('/brokers/', data=test_data, follow_redirects=True)
    assert response.status_code == 200
    
    # Verify the broker was added to the database
    with client.application.app_context():
        broker = Broker.query.filter_by(name='Test Broker').first()
        assert broker is not None
        assert broker.email == 'test@example.com'
        assert broker.webpage == 'http://test.com'

def test_broker_form_validation(client):
    """Test that the form validates correctly"""
    # Test with invalid data (empty name)
    test_data = {
        'name': '',
        'email': 'test@example.com',
        'webpage': 'http://test.com'
    }
    
    response = client.post('/brokers/', data=test_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'This field is required' in response.data

def test_broker_list_display(client):
    """Test that brokers are displayed on the page"""
    # Add a test broker
    with client.application.app_context():
        broker = Broker(
            name='Display Test Broker',
            email='display@example.com',
            webpage='http://display.com'
        )
        db.session.add(broker)
        db.session.commit()
    
    # Check if the broker appears on the page
    response = client.get('/brokers/')
    assert b'Display Test Broker' in response.data
    assert b'display@example.com' in response.data
    assert b'http://display.com' in response.data 