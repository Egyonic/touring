from random import randint,random
from sqlalchemy.exc import IntegrityError
from faker import Faker
from random import randint
from . import db
from .models import User, Journey, Activity, Label, BillInfo, BillItem


def fake_users(count=50):
    fake = Faker('zh_cn')
    i = 0
    while i < count:
        u = User(name=fake.user_name(),
                 email=fake.email(),
                 password='password',
                 confirmed=True,
                 )
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def journeys(count=50):
    fake = Faker('zh_cn')
    users = User.query.all()
    uids = [u.id for u in users]
    length = len(uids)
    i = 0
    while i < count:
        journey = Journey(name=fake.name(),
                          owner_id=randint(1, length),
                          destination=fake.city(),
                          budget=random()*5000,

                          )

