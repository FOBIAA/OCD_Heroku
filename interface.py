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
        return Award.query.filter_by(image=image).first().name

    def get_achievements(self):
        if self.achievements is None:
            from models import Achieved
            self.achievements = Achieved.query.filter_by(client=session["username"])
        return self.achievements

    def get_leaderboard_snippet(self):
        if self.snippet is None:
            from models import Client
            leaderboard = Client.query.order_by(Client.score.desc()).all()
            self.snippet = []
            self.rank = [0, 0]
            for client in leaderboard:
                if client.username == session["username"]:
                    break
                self.rank[0] += 1
            self.rank[1] = self.rank[0] + 1

            if self.rank[0] + 1 == len(leaderboard):
                self.rank[0] -= 3
            elif self.rank[0] >= 2:
                self.rank[0] -= 2
            elif self.rank[0] == 1:
                self.rank[0] -= 1

            for i in range(4):
                self.snippet.append(leaderboard[self.rank[0]])
                self.rank[0] += 1
        return self.snippet

    def get_full_leaderboard(self):
        if self.leaderboard is None:
            from models import Client
            self.leaderboard = Client.query.order_by(Client.score.desc())
        return self.leaderboard

    def get_rank(self):
        if self.rank is None:
            self.get_leaderboard_snippet()
        return [self.rank[0] - 3, self.rank[1]]

    def check_awards(self):
        from web import db
        from models import Achieved, Donation
        self.get_donations()
        donations = self.donations
        client = self.get_client()
        rank = self.get_rank()[1]
        time = donations.order_by(Donation.date.desc()).first().date - \
            donations.order_by(Donation.date).first().date
        rules = {"donor": donations.first() is not None, "contributor": donations.count() > 10,
                 "keeper": donations.count() > 50, "3rd": rank <= 3, "2nd": rank <= 2, "1st": rank == 1,
                 "appreciated": time.days > 7, "noble": time.days > 30, "dedicated": time.days > 365,
                 "generous": client.score > 250, "master": client.score > 500, "king": client.score > 2000}
        for award, condition in rules.items():
            if self.get_achievements().filter_by(award=award).first() is None and condition:
                db.session.add(Achieved(client.username, award))
        db.session.commit()

    def get_progress(self):
        from models import Donation
        self.get_donations()
        donations = self.donations
        score = self.get_client().score
        count = self.get_full_leaderboard().count()
        rank = count - self.get_rank()[1] + 1
        time = donations.order_by(Donation.date.desc()).first().date - \
            donations.order_by(Donation.date).first().date
        measures = [[("donor", 0), ("contributor", donations.count() / 10), ("keeper", donations.count() / 50)],
                    [("3rd", rank / (count - 2)), ("2nd", rank / (count - 1)), ("1st", rank / count)],
                    [("appreciated", time.days / 7), ("noble", time.days / 30), ("dedicated", time.days / 365)],
                    [("generous", score / 250), ("master", score / 500), ("king", score / 2000)]]
        progress = {}

        for measure in measures:
            for award, exp in measure:
                if self.get_achievements().filter_by(award=award).first() is None:
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
