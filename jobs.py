'''
#
# Website about jobs in VietNam
# author: hophamtenquang
#
'''
from flask import Flask, render_template
import sqlite3
import datetime
app = Flask(__name__)

@app.route('/')
def hello():
	return 'Hello'

@app.route('/jobs')
def index():
	con = sqlite3.connect('jobs.db')
	jobs = con.execute('select id, title, date_create, path from jobs order by date_create desc')
	return render_template('index.html', jobs=[row for row in jobs])

@app.route('/jobs/detail/<id>')
def detail(id):
	con = sqlite3.connect('jobs.db')
	cur = con.cursor()
	cur.execute('select id, title, date_create, path, detail from jobs where id = ?', (id,))
	job = cur.fetchone()
	return render_template('detail.html', job=job)

if __name__ == "__main__":
    app.run(debug=True)
