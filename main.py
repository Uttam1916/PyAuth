from flask import Flask, render_template, redirect , session ,request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key="mysecretkey"

#configure sql database
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= False
db=SQLAlchemy(app)

#database model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password_hash = db.Column(db.String(150), nullable=False)


    def set_password(self,password):
        self.password_hash=generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

#home
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")

#login
@app.route("/login",methods=["POST"])
def login():
    username=request.form("username")
    password_hash=request.form("password")
    user= Users.query.filter_by("username")
    if user and user.check_password(password):
        session["username"]=user
        return redirect(url_for("dashboard"))
    else:
        return render_template("index.html")

#register
@app.route("/register",methods=["POST"])
def register():
    username=request.form("username")
    password_hash=request.form("password")
    user= Users.query.filter_by("username")
    if user:
        return render_template("index.html",error="user already exists!")
    else:
        newUser= User(username=username)
        newUser.set_password(password)
        db.session.add(newUser)
        db.session.commit()
        session["username"]=user
        return redirect(url_for("dashboard"))




if __name__ == "__main__":  
    with app.app_context():
        db.create_all()
    app.run(debug=True)
