from flask import Flask
from flask import render_template, redirect
import random

app = Flask(__name__)


@app.route("/")
def index():
    return redirect("/" + str(random.randint(0, 2 ** (8 ** 2))))


@app.route("/<int:id>")
def canvas(id):
    return render_template("canvas.html")
