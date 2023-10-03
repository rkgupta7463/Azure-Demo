from flask import Flask, render_template, request, flash, redirect, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Replace with your actual secret key
app.secret_key = 'jhbfbbvibrkskfbdn(rishukumargupta8409+('

# Configure the database URI. You can replace 'sqlite:///mydatabase.db' with your preferred database URI.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///doubt.db'


# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define your database model


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    message = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        name = request.form.get('name')
        messages = request.form.get('messages')

        # Check if the username already exists in the database
        existing_user = Message.query.filter_by(name=name).first()

        if existing_user:
            flash("This username already exists! Just you can update message or delete below message! or you use different username!😒")
            return redirect('/')

        # If the username is unique, create a new user and add to the database
        message_db = Message(name=name, message=messages, date=datetime.now())
        db.session.add(message_db)
        db.session.commit()

        flash("Data has inserted into DB!👏")
        return redirect('/')

    user_fetched_data = None
    usersData = Message.query.all()
    if len(usersData) > 0:
        user_fetched_data = usersData

    # Get the flashed messages and pass them to the template
    messages = get_flashed_messages()

    return render_template("index.html", messages=messages, user_fetched_data=user_fetched_data)


@app.route("/delete/<int:message_id>", methods=['GET', 'POST'])
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    flash("Message deleted successfully!👏")
    return redirect('/')


@app.route("/update/<int:message_id>", methods=['GET', 'POST'])
def update_message(message_id):
    # Get the message from the database by message_id
    message = Message.query.get_or_404(message_id)

    if request.method == "POST":
        name = request.form.get('name')
        new_message = request.form.get('messages')

        # Update the message content with the new_message
        message.name = name
        message.message = new_message
        db.session.commit()
        flash("Message updated successfully!😎")
        return redirect('/')

    return render_template("index.html", message=message)


if __name__ == "__main__":
    # Create the table within the application context
    with app.app_context():
        db.create_all()

    app.run(debug=True, host="0.0.0.0")
