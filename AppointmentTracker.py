from flask import Flask, render_template, request, json
from flaskext.mysql import MySQL
from datetime import date, datetime

app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin00'
app.config['MYSQL_DATABASE_DB'] = 'Appointments'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

dbConnection = mysql.connect()
dbCursor = dbConnection.cursor()

@app.route('/')
def hello_world():
    return render_template('index.html')
	
@app.route('/createAppForm')
def display_form():
	return render_template('createAppointment.html')

@app.route('/makeApp', methods=['POST'])
def addAppointment():
	_title = request.form['nameIn']
	_subtitle = request.form['subnameIn']
	_attendees = request.form['attendeesIn']
	_date = request.form['dateIn']
	_time = request.form['timeIn']
	
	if not ( _title and _subtitle and _attendees and _date and _time ):
		return json.dumps({'html':'<span>Please fill all fields.</span>', 'title':_title, 'subtitle':_subtitle, 'attendees':_attendees, 'date':_date, 'time':_time})
	else:
		dbCursor.callproc('sp_makeAppointment', (_title, _subtitle, _attendees, _date, _time))
		dbOut = dbCursor.fetchall()
		
		if len(dbOut) is 0:
			dbConnection.commit()
			return json.dumps({'message':'Appointment added!'})
		else:
			return json.dumps({'error':str(data[0])})


@app.route('/seeApps')
def display_view():
	return render_template('viewAppointments.html')

@app.route('/viewApps', methods=['POST'])
def displayItems():
	dbCursor.execute("SELECT * FROM AppointmentData")
	dbOut = dbCursor.fetchall()
	print(dbOut)
	niceForm = ''
	for i in dbOut:
		niceForm += ('Name: ' + i[1] + '<br>Subname: ' + i[2] + '<br>Attendees: ' + i[3] + '<br>Date: ' + str(i[4]) + '<br>Time: ' + str(i[5]) + '<br><br>')
	return niceForm

@app.route('/removeApps', methods=['POST'])
def delRecords():
	print('Deletion attempted!')
	dbCursor.execute("DELETE FROM AppointmentData")
	dbOut = dbCursor.fetchall()
	
	if len(dbOut) is 0:
		dbConnection.commit()
		return json.dumps({'message':'Deletion confirmed!'})
	else:
		return json.dumps({'error':str(data[0])})
	
	
@app.route('/viewTest')
def test_title():
	return json.dumps('Hello World!')
	

if __name__ == "__main__":
    app.run()
