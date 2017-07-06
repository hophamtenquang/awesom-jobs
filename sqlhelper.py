import sqlite3
import json
from datetime import datetime

with open('jobs.json') as input:
    data = json.load(input)
con = sqlite3.connect("jobs.db")
# con.execute('''create table jobs (
#     id integer primary key,
#     date_create datetime,
#     title varchar(500),
#     detail varchar(500),
#     path varchar(200)
#     )''')
# con.execute('delete from jobs')
job = []
for key in data:
    date_create = datetime.strptime(data[key][1], '%b %d, %Y')
    job.append([key, date_create, data[key][0], data[key][3],data[key][2]] )
try:
    con.executemany("insert into jobs values (?, ?, ?, ?, ?)", job)
except sqlite3.IntegrityError:
    pass
con.commit()

# Print the table contents
for row in con.execute("select id, title, date_create from jobs order by date_create desc"):
    print(row[2])
