'''
Test requirements according to R6
'''

from unittest.mock import patch

from qa327_test.conftest import base_url
from werkzeug.security import generate_password_hash
from qa327_test.frontend.geek_base import GeekBaseCase, TEST_USER, TEST_TICKET
from qa327.models import User
from qa327.ticket_format import parse_date

INVALID_NAMES = ['special^char', 'ticket ', ' ticket', 'loooooooooooooooooooooooooooooooooooooooooooooooooooooooooongname']

INVALID_QUANTITY = [-1, 101]

BAD_USER = User(
    email='test_frontend@test.com',
    name='test_frontend',
    password=generate_password_hash('test_frontend'),
    balance=10
)

class R6Test(GeekBaseCase):

    @patch('qa327.backend.get_user', return_value=TEST_USER)
    def invalid_ticketname(self, *_):
        '''
        see r6.1.2, r6.1.4, r6.2.2- negative
        ensure ticket name is alphanumeric only, 
        space only allowed in the middle
        '''
        self.login_test_user()
        self.open(base_url)
        for name in INVALID_NAMES:
            self.input('#buy-ticket-name', name)
            self.input('#buy-ticket-quantity', TEST_TICKET.quantity)
            self.click('#buy-submit')
            self.assert_flash('Invalid ticket name')
            self.get_current_url() == base_url+'/'

    @patch('qa327.backend.get_user', return_value=TEST_USER)
    def test_invalid_quantity(self, *_):
        '''
        see r6.3.2 - negative
        ensure ticket quantity is > 0 and <= 100
        '''
        self.login_test_user()
        self.open(base_url)
        for name in INVALID_QUANTITY:
            self.input('#buy-ticket-name', TEST_TICKET.name)
            self.input('#buy-ticket-quantity', TEST_TICKET.quantity)
            self.click('#buy-submit')
            self.assert_flash('Invalid ticket quantity')
            self.get_current_url() == base_url+'/'

    @patch('qa327.backend.get_user', return_value=TEST_USER)
    @patch('qa327.backend.get_ticket', return_value=TEST_TICKET)
    def ticket_exists(self, *_):
        '''
        see r6.4.2 - negative
        ensure ticket exists in DB
        '''
        self.login_test_user()
        self.open(base_url)
        self.input('#buy-ticket-name', 'wontexist')
        self.input('#buy-ticket-quantity', str(TEST_TICKET.quantity))
        self.click('#buy-submit')
        self.assert_flash('No such ticket exists')
        self.get_current_url() == base_url+'/'

    @patch('qa327.backend.get_user', return_value=TEST_USER)
    @patch('qa327.backend.get_ticket', return_value=TEST_TICKET)
    def ticket_quant(self, *_):
        '''
        see r6.4.4 - negative
        ensure enough tickets in DB
        '''
        self.login_test_user()
        self.open(base_url)
        self.input('#buy-ticket-name', TEST_TICKET.name)
        self.input('#buy-ticket-quantity', str(TEST_TICKET.quantity + 10))
        self.click('#buy-submit')
        self.assert_flash('Not enough tickets available')
        self.get_current_url() == base_url+'/'

    @patch('qa327.backend.get_user', return_value=BAD_USER)
    @patch('qa327.backend.get_ticket', return_value=TEST_TICKET)
    def invalid_balance(self, *_):
        '''
        see r6.4.4 - negative
        ensure enough money to buy tickets
        '''
        self.login_test_user()
        self.open(base_url)
        self.input('#buy-ticket-name', TEST_TICKET.name)
        self.input('#buy-ticket-quantity', '1')
        self.click('#buy-submit')
        self.assert_flash('Account balance is too low')
        self.get_current_url() == base_url+'/'

    @patch('qa327.backend.get_user', return_value=TEST_USER)
    @patch('qa327.backend.get_ticket', return_value=TEST_TICKET)
    def buy_ticket_success(self, *_):
        '''
        see r6.1 - r.6 - positive
        ensures a ticket meeting all the requirements can be bought
        '''
        self.login_test_user()
        self.open(base_url)
        self.input('#buy-ticket-name', TEST_TICKET.name)
        self.input('#buy-ticket-quantity', '1')
        self.click('#buy-submit')
        self.assert_flash('Ticket bought successfully')

