#!/usr/bin/env python

from flask import session


class Interface:
    # Initialize basic class variables
    def __init__(self):
        self.client = None
        self.charities = None
        self.targets = None
        self.donations = None

    def get_client(self):
        if self.client is None:
            from models import Client
            self.client = Client.query.get(session["username"])
        return self.client

    def get_charities(self):
        if self.charities is None:
            from models import Charity, DonatesTo
            self.charities = []
            for target in Charity.query.join(DonatesTo).filter_by(client=session["username"]):
                self.charities.append(target)
            for charity in Charity.query:
                if charity not in self.charities:
                    self.charities.append(charity)
        return self.charities

    def get_targets(self):
        if self.targets is None:
            from models import DonatesTo
            self.targets = DonatesTo.query.filter_by(client=session["username"])
        return self.targets

    def get_donations(self):
        if self.donations is None:
            from models import Donation
            self.donations = Donation.query.filter_by(client=session["username"])
        return self.donations

    def refresh(self):
        self.client = None
        self.charities = None
        self.targets = None
        self.donations = None
