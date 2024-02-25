from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
# Declare a base class for declarative class definitions
Base = declarative_base()

from sqlalchemy import DateTime
from sqlalchemy.sql import func

class Plant(Base):
    __tablename__ = 'plants'
    id = Column(Integer, Sequence('plant_id_seq'), primary_key=True)
    name = Column(String(50))
    last_watered = Column(DateTime, server_default=func.now())


# class Disease(Base):
#     __tablename__ = 'diseases'
#     id = Column(Integer, Sequence('disease_id_seq'), primary_key=True)
#     name = Column(String(50))
#     timestamp = Column(DateTime, server_default=func.now())
#     image_path = Column(String(255))

class Disease(Base):
    __tablename__ = 'diseases'
    id = Column(Integer, Sequence('disease_id_seq'), primary_key=True)
    name = Column(String(50))
    timestamp = Column(DateTime, server_default=func.now())
    plant_ids = Column(String(50), default=[])

    def add_plant_id(self, plant_id):
        if plant_id not in self.plant_ids:
            self.plant_ids.append(plant_id)



if __name__=="__main__":
    # Create an SQLite database file
    engine = create_engine('sqlite:///example.db', echo=True)

    # Create the table in the database
    Base.metadata.create_all(engine)

    # Create a session to interact with the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Add users to the database
    # User.add_user(session, 'John Doe', 30)
    # User.add_user(session, 'Jane Smith', 25)

    # # Retrieve and print all users from the database
    # all_users = User.get_all_users(session)
    # for user in all_users:
    #     print(f"User ID: {user.id}, Name: {user.name}, Age: {user.age}")

    # # Remove a user from the database (change the user_id as needed)
    # User.remove_user(session, 1)

    # # Close the session
    session.close()
