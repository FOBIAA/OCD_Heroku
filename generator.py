from random import sample, randint as rand, seed
from requests import get
from json import loads
from os import listdir
script = open('script.py', 'w+')
print = lambda string: script.write(string + '\n')
add = 'db.session.add({})'.format
names_url = 'https://raw.githubusercontent.com/dominictarr/random-name/master/first-names.txt'
__names = []


def __get_names(count):
    if not __names:
        __names.extend(filter(lambda n: len(n) < 12, get(names_url).text.split()))
    seed(0)
    return sample(__names, k=count)


def __get_charities():
    with open('static/img/charity/details.json') as charity:
        return loads(charity.read())


def clients(count):
    emails = ['gmail', 'hotmail', 'outlook', 'ymail', 'yahoo']
    print('from models import Client')
    for name in __get_names(count):
        print(add(f'Client("{name}", "{name.upper()}123", "{name.lower()}@{sample(emails, k=1)[0]}.com", {rand(30000, 90000)})'))


def charities():
    print('from models import Charity')
    for img, charity in __get_charities().items():
        print(add(f'Charity("{charity["name"]}", "{img}.jpg", "{charity["desc"]}")'))


def awards():
    print('from models import Award')
    path, details = 'static/img/award/', 'details.json'
    for desc, img in zip(loads(open(path + details).read()), filter(details.__ne__, listdir(path))):
        prefix = 'The ' if len(img) <= 10 else ''
        print(add(f'Award("{prefix + img[:-4].capitalize()}", "{img}", "{desc}")'))


def donates_tos(count):
    print('from models import DonatesTo')
    _charities = __get_charities().keys()
    for name in __get_names(count):
        for charity in sample(_charities, k=rand(1, 4)):
            print(add(f'DonatesTo("{name}", "{charity}")'))


def donations(count, year=2018):
    print('from models import Donation')
    print('from datetime import datetime as date')
    for name in __get_names(count):
        for _ in range(rand(0, 15)):
            print(add(f'Donation("{name}", date({year}, {rand(1, 12)}, {rand(1, 28)}), {rand(1, 200) * 10})'))


if __name__ == '__main__':
    print('from web import db')
    clients_count = 50

    clients(clients_count)
    charities()
    awards()

    donates_tos(clients_count)
    donations(clients_count)
    print('db.session.commit()')
