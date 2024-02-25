# Function to add a plant to the database
from sql_alcmehy_model import Plant
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import json
from datetime import datetime
# Create an SQLite database file
engine = create_engine('sqlite:///example.db', echo=True)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

def add_plant(plant_id, name):
    new_plant = Plant(plant_id=json.dumps(plant_id), name=name)
    session.add(new_plant)
    session.commit()

def water_plant(plant_id):
    # Get the plant from the database
    plant = session.query(Plant).get(plant_id)
    if plant:
        plant.last_watered = datetime.now()
        session.commit()
    else:
        print("Plant not found")
    

def get_all_plants():
    return [{'id':i.id, 'plant_id': i.plant_id, "timestamp": i.timestamp, "name": i.name} for i in session.query(Plant).all()]

def get_one_plant(plant_id):
    return [{'id':i.id, 'plant_id': i.plant_id, "timestamp": i.timestamp, "name": i.name} for i in session.query(Plant).filter(Plant.plant_id == plant_id).all()]
    


add_plant(plant_id=[1,2.2], name="Tomato")
a=get_all_plants()
get_one_plant(a[-1]['plant_id'])
water_plant(1)
# a[-1]['id']