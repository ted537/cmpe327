import pytest
from seleniumbase import BaseCase
from unittest.mock import patch
from qa327_test.conftest import base_url
from qa327.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

# Moch a sample user
test_user = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend')
)

# Moch some sample tickets
test_tickets = [
    {'name': 't1', 'price': '100'}
]

class R3Test(BaseCase):

    def test_login_redirects(self, *_):
        '''
        see r3.1
        '''
        # open home page
        self.open(base_url)
        # verify redirected to /login
        assert self.get_current_url() == base_url+'/login'
        self.assert_element('#login_input')

    @patch('qa327.backend.get_user', return_value=test_user)
    def test_hi_user(self,*_):
        '''
        see r3.2
        '''
        # open home page
        self.open(base_url)
        self.assert_text('Hi test_frontend','#header')