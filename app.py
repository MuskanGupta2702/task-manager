from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

IST = pytz.timezone('Asia/Kolkata')

class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    user_name = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(120), nullable = False)
    password = db.Column(db.String(60),nullable = False)

    def __repr__(self):
        return f"{self.user_name}"

class Task(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    task = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.now(IST))
    completed = db.Column(db.Integer,default = 0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    user = db.relationship('User',backref=db.backref('task', lazy=True))
    
    def __repr__(self):
        return f"{self.task}"

@app.route('/')
def home():
    return "<h1>Task Manager</h1>"


if __name__ == '__main__':
    app.run(debug=True)