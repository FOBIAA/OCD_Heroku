#!/usr/bin/env python

# Import needed libraries
from web import db


# Database schema class for client
class Client(db.Model):
    # Declare table name as clients
    __tablename__ = "client"

    # Declare client's username as primary key
    username = db.Column(db.String(16), primary_key=True)
    # Declare other client fields
    password = db.Column(db.String(16))
    email = db.Column(db.String(24))
    balance = db.Column(db.Float)
    rank = db.Column(db.Integer)
    score = db.Column(db.Integer)
    type = db.Column(db.String(8))
    amount = db.Column(db.Float)
    frequency = db.Column(db.Integer)

    # Initialize class with basic info
    def __init__(self, username, password, email, balance):
        self.username = username
        self.password = password
        self.email = email
        self.balance = balance
        self.score = 0
        self.rank = None
        self.type = None
        self.amount = None
        self.frequency = None

    # Print class as < username >
    def __repr__(self):
        return "< " + self.username + " >"


class DonatesTo(db.Model):
    # Declare table name as donates_to
    __tablename__ = "donates_to"

    # Declare client's username and charity's name as primary key
    client = db.Column(db.String(16), db.ForeignKey("client.username"), primary_key=True)
    charity = db.Column(db.String(36), db.ForeignKey("charity.name"), primary_key=True)

    # Initialize class with client and charity
    def __init__(self, client, charity):
        self.client = client
        self.charity = charity


class Charity(db.Model):
    # Declare table name as charity
    __tablename__ = "charity"

    # Declare charity's name as primary key
    name = db.Column(db.String(36), primary_key=True)
    # Declare other charity fields
    image = db.Column(db.String(16))
    description = db.Column(db.Text)
    investment = db.Column(db.Text)

    # Initialize class with basic info
    def __init__(self, name, image, description, investment=None):
        self.name = name
        self.image = image
        self.description = description
        self.investment = investment

    # Print class as < name >
    def __repr__(self):
        return "<" + self.name + ">"


class Achieved(db.Model):
    # Declare table name as achieved
    __tablename__ = "achieved"

    # Declare client's username and award's name as primary key
    client = db.Column(db.String(16), db.ForeignKey("client.username"), primary_key=True)
    award = db.Column(db.String(36), db.ForeignKey("award.name"), primary_key=True)

    # Initialize class with client and award
    def __init__(self, client, award):
        self.client = client
        self.award = award


class Award(db.Model):
    # Declare table name as award
    __tablename__ = "award"

    # Declare award's name as primary key
    name = db.Column(db.String(36), primary_key=True)
    # Declare other award fields
    image = db.Column(db.String(16))
    description = db.Column(db.Text)

    # Initialize class with basic info
    def __init__(self, name, image, description):
        self.name = name
        self.image = image
        self.description = description

    # Print class as < name >
    def __repr__(self):
        return "<" + self.name + ">"


class Donation(db.Model):
    # Declare table name as donation
    __tablename__ = "donation"

    # Declare donation's date as primary key
    date = db.Column(db.DateTime, primary_key=True)
    # Declare other donation fields
    amount = db.Column(db.Float)
    client = db.Column(db.String(16), db.ForeignKey("client.username"))

    # Initialize class with date, amount and client username
    def __init__(self, client, date, amount):
        self.date = date
        self.amount = amount
        self.client = client

    # Print class as < username, Date: date >
    def __repr__(self):
        return "< " + self.client + ", Date: " + self.date.ctime() + " >"
