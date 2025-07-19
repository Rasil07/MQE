# app/routes.py
from flask import Blueprint, render_template, request
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html', title='MQE')


