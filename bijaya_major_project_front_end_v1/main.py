from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os, json

from sql_alcmehy_model import Plant, Disease

app = Flask(__name__)

# Create an SQLite database file
engine = create_engine('sqlite:///example.db', echo=True)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()
# Function to upload images and return the path
def upload_image(file):
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('static', filename)
        file.save(file_path)
        return file_path
    return None

# Route to add a new plant
@app.route('/add_plant', methods=['POST'])
def add_plant():
    if request.method == 'POST':
        name = request.form['name']
        new_plant = Plant(name=name)
        session.add(new_plant)
        session.commit()
        return redirect(url_for('display_plants'))


# # Route to add disease information
# @app.route('/add_disease', methods=['POST'])
# def add_disease():
#     if request.method == 'POST':
#         name = request.form['name']
#         image = request.files['image']
#         image_path = upload_image(image)
#         new_disease = Disease(name=name, image_path=image_path)

#         # Add plant_id to the disease (replace 1.0 with the actual plant_id)
#         plant_id = float(request.form['plant_id'])
#         new_disease.add_plant_id(plant_id)

#         session.add(new_disease)
#         session.commit()
#         return redirect(url_for('display_diseases'))

# Route to water a plant
@app.route('/water_plant/<int:plant_id>', methods=['POST'])
def water_plant(plant_id):
    if request.method == 'POST':
        plant = session.query(Plant).get(plant_id)
        if plant:
            plant.last_watered = datetime.now()
            session.commit()
    return redirect(url_for('display_plants'))

# Route to delete a plant
@app.route('/delete_plant/<int:plant_id>', methods=['POST'])
def delete_plant(plant_id):
    if request.method == 'POST':
        plant = session.query(Plant).get(plant_id)
        if plant:
            session.delete(plant)
            session.commit()
    return redirect(url_for('display_plants'))



# Route to add disease information
@app.route('/add_disease', methods=['POST'])
def add_disease():
    if request.method == 'POST':
        name = request.form['name']
        plant_id = request.form['plant_id']
        print(' \n\n\n\n\n',plant_id, name, type(plant_id), type(name))
        # image = request.files['image']
        # image_path = upload_image(image)
        new_disease = Disease(name=name, plant_ids=json.dumps(plant_id))# , image_path=image_path)
        session.add(new_disease)
        session.commit()
        return redirect(url_for('display_diseases'))

# Route to delete a disease
@app.route('/delete_disease/<int:disease_id>', methods=['POST'])
def delete_disease(disease_id):
    if request.method == 'POST':
        disease = session.query(Disease).get(disease_id)
        if disease:
            session.delete(disease)
            session.commit()
    return redirect(url_for('display_diseases'))


# Route to display all plants
@app.route('/display_plants')
def display_plants():
    all_plants = session.query(Plant).all()
    return render_template('plants.html', plants=all_plants)

# Route to display all diseases
@app.route('/display_diseases')
def display_diseases():
    all_diseases = session.query(Disease).all()
    return render_template('diseases.html', diseases=all_diseases)


if __name__ == '__main__':
    app.run(debug=True)
