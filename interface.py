#!/usr/bin/env python
from __future__ import division
from flask import session


class Interface:
    def __init__(self):
        self.client = None
        self.charities = None
        self.targets = None
        self.donations = None
        self.awards = None
        self.achievements = None
        self.snippet = None
        self.leaderboard = None
        self.rank = None

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
        from models import Donation
        if self.donations is None:
            self.donations = Donation.query.filter_by(client=session["username"])
        return self.donations.order_by(Donation.date.desc())

    def get_awards(self):
        if self.awards is None:
            from models import Award
            self.awards = Award.query
        return self.awards

    @staticmethod
    def get_awards_by_image(image):
        from models import Award
        return Award.query.filter_by(image=image).first()

    @staticmethod
    def get_charity_by_image(image):
        from models import Charity
        return Charity.query.filter_by(image=image).first()

    def get_achievements(self):
        if self.achievements is None:
            from models import Achieved
            self.achievements = Achieved.query.filter_by(client=session["username"])
        return self.achievements

    def get_leaderboard_snippet(self, index):
        if self.snippet is None:
            self.snippet = self.get_full_leaderboard().all()[index: index + 4]
        return self.snippet

    def get_full_leaderboard(self):
        if self.leaderboard is None:
            from models import Client
            self.leaderboard = Client.query.filter_by(reveal="true").order_by(Client.score.desc())
        return self.leaderboard

    def get_rank(self):
        if self.rank is None:
            if self.get_client().reveal == "true":
                try: self.rank = self.get_full_leaderboard().all().index(self.get_client()) + 1
                except:
                    print('ERROR: out of index while getting rank, list:', str(self.get_full_leaderboard().all()))
                    self.rank = 1
            else:
                self.rank = -1
        return self.rank

    def get_time(self):
        if self.donations.first() is not None:
            from models import Donation
            return self.donations.order_by(Donation.date.desc()).first().date - \
                self.donations.order_by(Donation.date).first().date
        else:
            from datetime import timedelta
            return timedelta(0)

    def check_awards(self):
        from web import db
        from models import Achieved
        donations = self.get_donations()
        client = self.get_client()
        rank = self.get_rank()
        time = self.get_time()
        rules = [("donor", donations.first() is not None), ("3rd", 3 >= rank > 0 and client.reveal),
                 ("appreciated", time.days > 7), ("generous", client.score > 250),
                 ("contributor", donations.count() > 10), ("2nd", 2 >= rank > 0 and client.reveal),
                 ("noble", time.days > 30), ("master", client.score > 500), ("keeper", donations.count() > 50),
                 ("1st", rank == 1 and client.reveal), ("dedicated", time.days > 365), ("king", client.score > 2000)]
        for award, condition in rules:
            if self.get_achievements().filter_by(award=award).first() is None and condition:
                db.session.add(Achieved(client.username, award))
        db.session.commit()

    def get_progress(self):
        donations = self.get_donations()
        score = self.get_client().score
        count = self.get_full_leaderboard().count()
        rank = count - self.get_rank() + 1 if self.get_rank() != count else 0
        time = self.get_time()
        measures = [[("donor", 0), ("contributor", donations.count() / 10), ("keeper", donations.count() / 50)],
                    [("3rd", rank / (count - 2)), ("2nd", rank / (count - 1)), ("1st", rank / count)],
                    [("appreciated", time.days / 7), ("noble", time.days / 30), ("dedicated", time.days / 365)],
                    [("generous", score / 250), ("master", score / 500), ("king", score / 2000)]]
        progress = {}

        for measure in measures:
            for award, exp in measure:
                if self.get_achievements().filter_by(award=award).first() is None:
                    if self.get_client().reveal == "false" and (award == "3rd" or award == "2nd" or award == "1st"):
                        break
                    progress[award] = int(exp * 100)
                    break
        return progress

    def refresh(self):
        self.client = None
        self.targets = None
        self.donations = None
        self.achievements = None
        self.snippet = None
        self.leaderboard = None
        self.rank = None
