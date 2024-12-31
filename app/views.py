from app import app
from flask import render_template

@app.route('/')
def tela_login():
    return render_template('login.html')