from flask import Flask,render_template,request,redirect,flash,session,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/?'
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

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['user_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password == confirm_password:
            if email != "" and password != "":
                existing_user = User.query.filter_by(email = email).first()
                if existing_user == None:
                    user = User(user_name = user_name,email = email,password = password)
                    db.session.add(user)
                    db.session.commit()
                    message = "Account Created Successfully!" 
                    # status = "success"
                    flash(message)
                    return redirect(url_for('login')) 
                else:
                    message = "Account already exists."
                    flash(message)
                    return redirect(url_for('register'))           
            else:
                message = "Please enter email and password!!"
                flash(message)
                return redirect(url_for('register'))       
        else:
            message = "Password didn't match" 
            flash(message)
            return redirect(url_for('register'))          
    else:
        return render_template('register.html')

@app.route('/login',methods =['POST','GET'])
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)