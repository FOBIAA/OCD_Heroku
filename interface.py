#!/usr/bin/env python

# from info import *
from flask import session


class Interface:
    # Initialize basic class variables
    def __init__(self):
        self.balance = None
        self.charities = None
        self.donations = None

    def get_balance(self):
        if self.balance is None:
            from models import Client
            self.balance = Client.query.get(session["username"]).balance
        return self.balance

    def get_charities(self):
        if self.charities is None:
            from models import Charity
            self.charities = Charity.query
        return self.charities

    def get_donations(self):
        if self.donations is None:
            from models import Donation
            self.donations = Donation.query.filter_by(client=session["username"])
        return self.donations

    def refresh(self):
        self.balance = None
        self.charities = None
        self.donations = None
