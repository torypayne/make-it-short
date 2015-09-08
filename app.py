from flask import Flask, render_template, redirect, request, url_for, flash, session
import requests
import json
import model
import ast
import datetime

app = Flask(__name__)
app.secret_key = 'thisisntarealsecretkeybecausethisisademo'



@app.route("/")
def index():
	return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
	app.run(debug = True)