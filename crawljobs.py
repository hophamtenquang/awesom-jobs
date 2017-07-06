from bs4 import BeautifulSoup
import requests
import html5lib
import json


URLS = [
    'https://github.com/awesome-jobs/vietnam/issues',
    #'https://github.com/awesome-jobs/vietnam/issues?page=2',
    #'https://github.com/awesome-jobs/vietnam/issues?page=3'
    ]
jobs = {}

def innerHTML(element):
    return element.decode_contents(formatter="html")

# Get all jobs in 3 page
for url in URLS:
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html5lib')
    for li in soup.select('ul.js-navigation-container li.js-issue-row'):
       job_name = li.select_one('a.link-gray-dark').text.strip()
       date_added = li.select_one('relative-time').text.strip()
       job_id = li.get('id').replace('issue_', '')
       detail_url = 'https://github.com/awesome-jobs/vietnam/issues/' + job_id
       resp_detail = requests.get(detail_url)
       soup_detail = BeautifulSoup(resp_detail.text, 'html5lib')
       job_detail = innerHTML(soup_detail.select_one('div.edit-comment-hide table'))
       jobs[job_id] = [job_name, date_added, detail_url, job_detail]
with open('jobs.json', 'w') as outfile:
    json.dump(jobs, outfile)
