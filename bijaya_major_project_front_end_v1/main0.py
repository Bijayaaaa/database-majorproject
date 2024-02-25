from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sql_alcmehy_model import User  # Replace 'your_module_name' with the actual module name

app = Flask(__name__)

# Create an SQLite database file
engine = create_engine('sqlite:///example.db', echo=True)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Route to display all users
@app.route('/')
def display_users():
    # Retrieve all users from the database using the User class
    all_users = User.get_all_users(session)
    
    # Render the template with the user data
    return render_template('users.html', users=all_users)

if __name__ == '__main__':
    app.run(debug=True)
