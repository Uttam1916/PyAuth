from flask import Flask, render_template, redirect, session, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_client import OAuth
from apikey import *

app = Flask(__name__)
app.secret_key = "mysecretkey"

oauth=OAuth(app)

# configure sql database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

google = oauth.register(
    name='google',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
    access_token_url='https://oauth2.googleapis.com/token',
    client_kwargs={'scope': 'openid profile email'},
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs', 
    api_base_url='https://www.googleapis.com/oauth2/v2/'
)


# database model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password_hash = db.Column(db.String(150), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# home
@app.route("/")
def home():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template("index.html")

# login
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session["username"] = user.username
        return redirect(url_for("dashboard"))
    else:
        return render_template("index.html", error="Invalid credentials")

# register
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(username=username).first()
    if user:
        return render_template("index.html", error="User already exists!")
    else:
        newUser = Users(username=username)
        newUser.set_password(password)
        db.session.add(newUser)
        db.session.commit()
        session["username"] = newUser.username
        return redirect(url_for("dashboard"))

# dashboard
@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return render_template("dashboard.html",username=session["username"])
    return redirect(url_for('home'))

#logout
@app.route("/logout")
def logout():
    session.pop("username")
    return redirect(url_for('home'))


#google login
@app.route("/login/google")
def login_google():
    try:
        redirect_uri = url_for('authorize_google',_external=True)
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        app.logger.error("login error : " ,e)
        return "error occurred during login",500

@app.route("/authorize/google")
def authorize_google():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    username = user_info['email']

    user = Users.query.filter_by(username=username).first()
    if not user:
        user = Users(username=username)
        db.session.add(user)
        db.session.commit()

    session['username'] = username
    session['oauth_token'] = token
    return redirect(url_for('dashboard'))


if __name__ == "__main__":  
    with app.app_context():
        db.drop_all()
        db.create_all()
    app.run(debug=True)
