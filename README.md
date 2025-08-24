# PyAuth

A simple **Flask-based authentication system** with **user registration, login, session management**, and modern styling using **Tailwind CSS**.

---

## Features

- User registration with **hashed passwords** (Werkzeug security).  
- User login with session management.  
- Protected dashboard accessible only to logged-in users.  
- Logout functionality.  
- Styled using **Tailwind CSS** for a clean, responsive UI.  

---

## Tech Stack

- **Backend:** Python, Flask  
- **Database:** SQLite (via SQLAlchemy ORM)  
- **Frontend:** HTML, Jinja2 Templates, Tailwind CSS  

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Uttam1916/PyAuth.git
cd PyAuth
```

2. Create a virtual environment and activate it:
```bash
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Running the App
```bash
python main.py
```
Open your browser at http://127.0.0.1:5000/home.
Register a new user or login with an existing account.