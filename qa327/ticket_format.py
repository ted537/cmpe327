"""helper functions for ticket format verification"""
import re
from datetime import datetime

def is_valid_ticket_name(ticket_name):
    """
    Validate ticket name with provided requirements
    :param ticket_name: ticket name of ticket trying to be registered
    :return: true if the username is acceptable, false otherwise
    """
    return (
        # ticket name has at least 6 characters, but no greater than 60
        6 <= len(ticket_name) <= 60 and
        # does not start or end with space
        ticket_name[0] != ' ' and
        ticket_name[-1] != ' ' and
        # is alphanumeric (plus space)
        bool(re.match(r'^[\w\d ]+$', ticket_name))
    )


def is_valid_quantity(quantity):
    """
    Validate quantity with provided requirements
    :param quantity: a interger for how many tickets the user wants to sell
    :return: true if the password is acceptable, false otherwise
    """
    # Verifies that quantity is an integer
    try:
        quantity = int(quantity)
        # Quantity is greater than 0 and less than 100
        return 0 < quantity <= 100
    except ValueError:
        return False


def is_valid_price(price):
    """
    Validate price with provided requirements
    :param price: a integer price for the ticket
    :return: true if the password is acceptable, false otherwise
    """
    # Verifies that price is an integer
    try:
        price = int(price)
        # Price must be at least $10 but no more than $100
        return 10 <= price <= 100
    except ValueError:
        return False


def is_valid_date(date):
    """
    Validate date with provided requirements
    :param date: a integer date for when the ticket is available for
    :return: true if the password is acceptable, false otherwise
    """
    date_format = '%Y%m%d'
    # Date must be in the correct format
    try:
        date = datetime.strptime(date, date_format)
        # Date must not have already passed
        return datetime.now() < date
    except ValueError:
        return False
