from flask import Flask, render_template, redirect, request, url_for, flash, session, jsonify
import requests
import json
import model
import datetime

app = Flask(__name__)
app.secret_key = 'thisisntarealsecretkeybecausethisisademo'


@app.route("/")
def index():
	return render_template("index.html")

@app.route("/new_code")
def new_code():
	url = request.args.get("url")
	model.db_connect()
	code = model.create_code(url)
	model.db.close()
	return render_template("new_code.html", url=url, code=code)

@app.route("/visits/<code>")
def url_visits(code):
	model.db_connect()
	url=model.url_info(code)
	model.db.close()
	return render_template("visits.html", url=url)

@app.route("/recent")
def recent_urls():
	model.db_connect()
	recent = model.recently_shortened()
	model.db.close()
	return render_template("recent.html", recent=recent)

@app.route("/popular")
def popular():
	model.db_connect()
	popular = model.most_popular()
	model.db.close()
	return render_template("popular.html", popular=popular)


@app.route("/<code>")
def redirect_on_code(code):
	try:
		model.db_connect()
		model.log_visit(code)
		url = model.url_info(code)
		model.db.close()
		return redirect(url.url)
	except:
		model.db.close()
		return render_template('404.html'), 404


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


if __name__ == "__main__":
	app.run(debug = True)