from flask import Flask, request, render_template, url_for
import os
import pymysql
import redis
import hashlib
import datetime
import json

app= Flask(__name__)
hostname = '<your hostname>'
username = '<username>'
password = '<password>'
database = '<db_name>'
r = redis.StrictRedis(host='<hostname>', port=<port_no>)
conn = pymysql.connect( host=hostname, port=<port_no>, user=username, passwd=password, db=database )
print ("conn success")
query="SELECT DateReceived, State, ZIP, Tags, Issue, Complaint_ID, Product FROM Consumer"
hashsqlquery = hashlib.md5(query).hexdigest()
print (hashsqlquery)
# Simple routine to run a query on a database and print the results:
cur = conn.cursor()
cached=r.get('hashv')
print(cached)
@app.route('/')
def index():
    return render_template('a4.html')

@app.route('/Cached', methods=['GET', 'POST'])
def cachedscreen():
	if cached==hashsqlquery:
		tstart=datetime.datetime.now()
		for i in range(5000):
			cachedresult=r.get(hashsqlquery)
		tend = datetime.datetime.now()
		diff=tend-tstart
		total=int(diff.total_seconds()*1000)
		print ("hashed"+str(total))
		return json.dumps({'data': str(total)}, 200, {'contentType': 'application/json'})
		# return render_template('time.html',total=total)

@app.route('/Uncached', methods=['GET', 'POST'])
def uncachedscreen():
	if request.method == 'POST':
     		r.set('hashv', hashsqlquery)
		tstart=datetime.datetime.now()
        	for i in range(5000):	
			cur.execute(query)
        	results = cur.fetchall()
        	tend = datetime.datetime.now()
		diff=tend-tstart
		total=int(diff.total_seconds()*1000)
        	print("unhashed"+str(total))
        	r.set(hashsqlquery, results)
        	print("hash succ")
        	return json.dumps({'data': str(total)}, 200, {'contentType': 'application/json'})
		# return render_template('time.html',total=total)
#port = os.getenv('VCAP_APP_PORT', '5500')

if __name__ == "__main__":
	app.run()
