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
    mock_get.assert_called_once_with('/tweets?skip=0&limit=5', headers={
                    'Authorization': 'Bearer ' + user.access_token
                })
    
    assert user.recent_tweets == mock_response_body
    assert tweets == {'body': mock_response_body, 'code': 200}

def test_post_tweets(mocker, user):
    mock_tweet = {'text': 'A Joke!'}
    mock_response_body = {'id': 1, 'text': 'A Joke!'}

    user.access_token = 'mock_access_token'
    mock_post = mocker.patch('util.NetworkRequest.post', return_value={
        'body': mock_response_body,
        'code': 201
    })
    tweets = user.post_tweets("A Joke!")
    mock_post.assert_called_once_with('/tweets', body=mock_tweet, headers={
                    'Authorization': 'Bearer ' + user.access_token
                })
    assert tweets == {'body': mock_response_body, 'code': 201}

def test_do_not_rotate_token_when_token_exist(mocker, user):
    
    mock_post = mocker.patch('util.NetworkRequest.post', side_effect=[
        {"code": 200, "body": []}
        ])
    
    user.access_token = 'mock_access_token'
    user.refresh_token = 'mock_refresh_token'

    tweets = user.post_tweets("A Joke!")
    
    assert mock_post.call_count == 1

def test_rotate_access_token_successful(mocker, user):
    mock_response = {
            "code": 201, 
            "body": {
                "id": 1, 
                "text": "mock_text",
            }}
    mock_post = mocker.patch('util.NetworkRequest.post', side_effect=[
        {"code": 401, "body": []},
        {"code": 200, "body": {
            "access_token": "mock_access_token", 
            "refresh_token": "mock_refresh_token",
            "token_type": "bearer"
            }},
        {"code": 201, "body": {
                "id": 1, 
                "text": "mock_text",
            }},
        ])
    
    user.access_token = 'mock_access_token'
    user.refresh_token = 'mock_refresh_token'

    tweets = user.post_tweets("mock_text")
    
    assert mock_post.call_count == 3
    assert tweets == mock_response

def test_rotate_access_token_unsuccessful(mocker, user):
    mock_post = mocker.patch('util.NetworkRequest.post', side_effect=[
        {"code": 401, "body": []},
        {"code": 401}
        ])
    
    user.access_token = 'mock_access_token'
    user.refresh_token = 'mock_refresh_token'

    tweets = user.post_tweets("mock_text")
    
    assert mock_post.call_count == 2
    assert tweets == {"code": 401, "body": []}
