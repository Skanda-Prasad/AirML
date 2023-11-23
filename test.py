import pytest
from streamlit.testing import TestClient
from streamlit.script_runner import TestClient
from finalcode import main  # Replace 'your_app_file' with the actual file name

@pytest.fixture
def client():
    return TestClient(main)

def test_login(client):
    # Test invalid login
    response = client.post_form('login_form', {'username': 'invalid_user', 'password': 'wrong_password'})
    assert 'Invalid Username or Password' in response.text

    # Test valid login
    response = client.post_form('login_form', {'username': 'valid_user', 'password': 'correct_password'})
    assert 'Login Successful!' in response.text

def test_admin_login(client):
    # Test invalid admin login
    response = client.post_form('login_form', {'admin_username': 'invalid_admin', 'admin_password': 'wrong_password'})
    assert 'Invalid Admin Username or Password' in response.text

    # Test valid admin login
    response = client.post_form('login_form', {'admin_username': 'valid_admin', 'admin_password': 'correct_password'})
    assert 'Admin Login Successful!' in response.text

def test_signup(client):
    # Test existing username
    response = client.post_form('signup_form', {'signup_username': 'existing_user', 'signup_password': 'password'})
    assert 'Username already exists' in response.text

    # Test new username
    response = client.post_form('signup_form', {'signup_username': 'new_user', 'signup_password': 'password'})
    assert 'Account created successfully!' in response.text
    assert 'You are now logged in.' in response.text

def test_aeroplane_testing(client):
    # Test aeroplane testing form
    response = client.post('/test-your-aeroplane', data={'time_in_cycles': 10, 'fan_inlet_temp': 300, 'core_speed': 100})
    assert 'Aircraft Safe!' in response.text

def test_upload_dataset(client):
    # Test dataset upload form
    response = client.post_form('Upload Dataset', {'uploaded_file': ('fake_dataset.csv', 'fake content')})
    assert 'File Uploaded Successfully!' in response.text

def test_manage_datasets(client):
    # Test manage datasets form
    response = client.post_form('Manage Datasets', {'selected_file': 'dataset_to_manage.csv', 'download': True})
    assert 'Download Successful!' in response.text

    response = client.post_form('Manage Datasets', {'selected_file': 'dataset_to_mark.csv', 'mark_as_complete': True})
    assert 'Dataset marked as complete!' in response.text

