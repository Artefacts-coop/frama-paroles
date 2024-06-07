from faker import Faker
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import create_engine


NB_CHANNELS = 10
NB_MEMBERS = 30
NB_POSTS = 100 # pour chaque membre

# Initialisation de la base de données
Base = declarative_base()


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    nickname = Column(String)
    gender = Column(String)
    etab = Column(String)

    def __repr__(self):
        return f"User {self.username}"


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"Channel {self.name}"


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    message = Column(String)
    member_id = Column(Integer, ForeignKey("members.id"))
    member = relationship("Member", backref="posts")
    channel_id = Column(Integer, ForeignKey("channels.id"))
    create_at = Column(Integer)
    

    def __repr__(self):
        return f"Post {self.post}"


# Créer la base de données
engine = create_engine("sqlite:///fake_data.sqlite")
Base.metadata.create_all(engine)

# Créer une session
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker("fr_FR")

# Ajouter des données à la base de données
for i in range(NB_MEMBERS):
    member = Member(
        username=f'{fake.first_name()}.{fake.last_name()}',
        nickname=fake.unique.name(),
        gender=fake.random_element(elements=("h", "f")),
        etab=fake.random_element(elements=("o", "t", "b", "n", "e")),
    )
    session.add(member)
    print(f"Member {member.username} added")

# Enregistrer les changements
session.commit()


# Créer les canaux
for i in range(1, NB_CHANNELS + 1):
    channel = Channel(id=i, name="_".join(fake.words(nb=2)))
    session.add(channel)
    print(f"Channel {channel.name} added")

# Enregistrer les changements
session.commit()


# Récupérer les membres
members = session.query(Member).all()

# Générer des posts pour chaque membre
for member in members:
    for i in range(NB_POSTS):
        post = Post(
            message=fake.sentence(),
            member_id=member.id,
            channel_id=fake.random_element(elements=range(1, NB_CHANNELS + 1)),
            create_at=fake.date_time_between(
                start_date="-4y", end_date="now"
            ).timestamp(),
        )
        session.add(post)
    print(f"Posts added for {member.username}")

# Enregistrer les changements
session.commit()

print("Done !")
