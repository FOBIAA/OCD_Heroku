#!/usr/bin/env python

# from info import *
from flask import session


class Interface:
    # Initialize basic class variables
    def __init__(self):
        self.balance = None
        self.charities = None

    def get_balance(self):
        if self.balance is None:
            from models import Client
            self.balance = Client.query.filter_by(username=session["username"]).first().balance
        return self.balance

    def get_charities(self):
        if self.charities is None:
            from models import Charity
            self.charities = Charity.query
        return self.charities


    def refresh(self):
        self.balance = None