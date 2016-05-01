#!/usr/bin/env python

from flask import session
from sqlalchemy import desc


class Interface:
    # Initialize basic class variables
    def __init__(self):
        self.client = None
        self.charities = None
        self.targets = None
        self.donations = None
        self.awards = None
        self.achievements = None

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

    def get_awards(self):
        if self.awards is None:
            from models import Award
            self.awards = Award.query
        return self.awards

    def get_achievements(self):
        if self.achievements is None:
            from models import Achieved
            self.achievements = Achieved.query.filter_by(client=session["username"])
        return self.achievements

    @staticmethod
    def check_awards():
        from web import db
        from models import Achieved, Donation, Client
        client = Client.query.get(session["username"])
        awards = Achieved.query.filter_by(client=session["username"])
        # Conditions for Awards by Number of Donations
        if awards.filter_by(award="donor").first() is None:
            if Donation.query.filter_by(client=session["username"]).first() is not None:
                db.session.add(Achieved(session["username"], "donor"))
        elif awards.filter_by(award="contributor").first() is None:
            if Donation.query.filter_by(client=session["username"]).count() > 25:
                db.session.add(Achieved(session["username"], "contributor"))
        elif awards.filter_by(award="keeper").first() is None:
            if Donation.query.filter_by(client=session["username"]).count() > 100:
                db.session.add(Achieved(session["username"], "keeper"))
        # Conditions for Awards by LeaderBoard Position
        top = Client.query.order_by(desc(Client.score)).limit(3).all()
        if awards.filter_by(award="3rd").first() is None and top[2] == client:
            db.session.add(Achieved(session["username"], "3rd"))
        if awards.filter_by(award="2nd").first() is None and top[1] == client:
            db.session.add(Achieved(session["username"], "2nd"))
        if awards.filter_by(award="1st").first() is None and top[0] == client:
            db.session.add(Achieved(session["username"], "1st"))
        # Conditions for Awards by Donating Period
        time = Donation.query.filter_by(client=session["username"]).order_by(desc(Donation.date)).first().date - \
               Donation.query.filter_by(client=session["username"]).order_by(Donation.date).first().date
        if awards.filter_by(award="appreciated").first() is None and time.days > 7:
            db.session.add(Achieved(session["username"], "appreciated"))
        elif awards.filter_by(award="noble").first() is None and time.days > 30:
            db.session.add(Achieved(session["username"], "noble"))
        elif awards.filter_by(award="dedicated").first() is None and time.days > 365:
            db.session.add(Achieved(session["username"], "dedicated"))
        # Conditions for Awards by Total Donation Amount
        if awards.filter_by(award="generous").first() is None and client.score > 250:
            db.session.add(Achieved(session["username"], "generous"))
        elif awards.filter_by(award="master").first() is None and client.score > 500:
            db.session.add(Achieved(session["username"], "master"))
        elif awards.filter_by(award="king").first() is None and client.score > 2000:
            db.session.add(Achieved(session["username"], "king"))
        db.session.commit()

    def refresh(self):
        self.client = None
        self.charities = None
        self.targets = None
        self.donations = None
        self.awards = None
        self.achievements = None
