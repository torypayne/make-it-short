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

@app.route("/new_code")
def new_code(url):
	url = request.args.get("url")
	model.db.connect()
	code = model.create_code(url)
	model.db.close()
	render_template("new_url.html", code=code, url=url)

@app.route("/<code>/visits")
def url_visits(code):
	model.db_connect()
	url_info=model.url_info(code)
	model.db.close()
	return render_template("visits.html", url_info=url_info)

@app.route("/recent")
def recent_urls():
	model.db_connect()
	recently_shortened = model.recently_shortened()
	model.db.close()
	return render_template("recently_shortened.html", recently_shortened=recently_shortened)

@app.route("/popular")
def popular():
	model.db_connect()
	most_popular = model.most_popular()
	model.db.close()
	return render_template("most_popular.html", most_popular=most_popular)





@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
	app.run(debug = True)