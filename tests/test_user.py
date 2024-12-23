from User import User
import pytest

@pytest.fixture()
def user():
    return User()

def test_save_token(user):
    tokens = {
        "access_token": "mock_access_token",
        "refresh_token": "mock_refresh_token",
        "token_type": "bearer"
    }
    user.save_tokens(tokens)
    assert user.access_token == "mock_access_token"
    assert user.refresh_token == "mock_refresh_token"
    assert user.token_type == "bearer"

def test_login_successful(mocker, user):
    body = {
        'access_token': 'test_access_token',
        'refresh_token': 'test_refresh_token',
        'token_type': 'Bearer'
    }
    mocker.patch('util.NetworkRequest.post', return_value={'body': body})
    mock_save_user = mocker.patch.object(user, 'save_tokens')
    mock_logger = mocker.patch('User.logger.debug')

    user.login('testuser', 'testpassword')
    
    mock_save_user.assert_called_once_with(body)
    mock_logger.assert_any_call('Log in successfull')

def test_login_unsuccessful(mocker, user):
    mock_post = mocker.patch('util.NetworkRequest.post', return_value={})

    mock_input = mocker.patch('builtins.input', side_effect=['Test', 'User'])
    mock_register = mocker.patch.object(user, 'register', return_value=None)

    user.login('testuser', 'testpassword')
    mock_register.assert_called_once_with('testuser', 'Test', 'User', 'testpassword')

def test_register_successful(mocker, user):
    mock_post = mocker.patch('util.NetworkRequest.post', return_value={'code':200})
    mock_login = mocker.patch.object(user, 'login', return_value=None)

    user.register('testuser', 'Test', 'User', 'testpassword')
    mock_login.assert_called_once_with('testuser', 'testpassword')

def test_register_unsuccessful(mocker, user):
    mock_post = mocker.patch('util.NetworkRequest.post', return_value={
        "code": 400,
        "message": "User Already Exist"
    })
    mock_login = mocker.patch.object(user, 'login', return_value=None)
    user.register('testuser', 'Test', 'User', 'testpassword')
    mock_login.assert_not_called()

def test_get_tweets(mocker, user):
    mock_response_body = [
        {'id': 1, 'content': 'First tweet'},
        {'id': 2, 'content': 'Second tweet'},
        {'id': 3, 'content': 'Third tweet'}
    ]
    user.access_token = 'mock_access_token'
    mock_get = mocker.patch('util.NetworkRequest.get', return_value={
        'body': mock_response_body,
        'code': 200
    })
    tweets = user.get_tweets()
    assert user.recent_tweets == mock_response_body
    assert tweets == {'body': mock_response_body, 'code': 200}

def test_post_tweets(mocker, user):
    mock_response_body = {'id': 1, 'content': 'First tweet'}
    user.access_token = 'mock_access_token'
    mock_post = mocker.patch('util.NetworkRequest.post', return_value={
        'body': mock_response_body,
        'code': 201
    })
    tweets = user.post_tweets("A Joke!")
    assert tweets == {'body': mock_response_body, 'code': 201}

def test_rotate_access_token_successful(mocker, user):

    mock_token_body = {
        'access_token': 'test_access_token',
        'refresh_token': 'test_refresh_token',
        'token_type': 'Bearer'
    }

    user.access_token = 'mock_access_token'
    user.refresh_token = 'mock_refresh_token'

    mock_save_user = mocker.patch.object(user, 'save_tokens')
    mock_post = mocker.patch('util.NetworkRequest.post', return_value={
        'body': mock_token_body,
        'code': 401
    })

    tweets = user.post_tweets("A Joke!")

    mock_save_user.assert_called_once_with(mock_token_body) 

def test_rotate_access_token_unsuccessful(mocker, user):
    pass