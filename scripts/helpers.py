import json
import jsonschema
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import datetime
import time
import os
import smtplib

try:
	#For version below 3.x
    from ConfigParser import SafeConfigParser
except ImportError:
	#For version 3.x and above
    from configparser import SafeConfigParser

try:
	#For version below 3.x
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    #from email.MIMEBase import MIMEBase
    #from email.Utils import COMMASPACE, formatdate
    from email import Encoders	
except ImportError:
	#For version 3.x and above
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    #from email.mime.Base import MIMEBase
    from email import encoders    
	
def log(msg, filename):
	time = datetime.datetime.now()
	timeString = str(time.year) + "/" + str(time.month).zfill(2) + "/" + str(time.day).zfill(2) + " " + str(time.hour).zfill(2) + ":" + str(time.minute).zfill(2) + "> "
	myLogFile = open(filename, 'r+') 
	myLogFile.seek(0)
	myLogFile.write(timeString + "\n" + msg + "\n")
	myLogFile.truncate()
	myLogFile.close()
	
def getWorkingDirectory():
	dirname, filename = os.path.split(os.path.abspath(__file__))
	#Go one level up the directory and return that path
	return os.path.dirname(dirname)
	#return dirname

def getUrlResponse(url):
	f = urllib.request.urlopen(url)
	charset = f.info().get_param('charset', 'utf8')
	data = f.read()
	response = json.loads(data.decode(charset))
	return response;
	
def getTodayDate():
	today = datetime.date.today()
	return today.strftime('%Y%m%d') #+ time.strftime("%H%M%S", time.gmtime(666))

def readConfig():
	parser = SafeConfigParser()
	dirPath = getWorkingDirectory()
	parser.read(dirPath + '/conf/conf.ini')
	return parser

parser = readConfig()

def sendMail(msg, sendOn):
	if sendOn != True:
		return

	msg = MIMEMultipart()
	msg["Subject"] = "API Automation test report"
	msg["From"] = parser.get("MAILING_DETAILS", "FROM")
	#msg['Date'] = formatdate(localtime=True)
	msg["To"] = parser.get("MAILING_DETAILS", "TO")
	body = MIMEText("This is an automated email.")
	msg.attach(body)
	
	smtp = smtplib.SMTP(parser.get("SMTP_DETAILS", "HOST"), parser.get("SMTP_DETAILS", "PORT"))
	smtp.ehlo()
	smtp.starttls()
	smtp.login(parser.get("SMTP_DETAILS", "USERNAME"), parser.get("SMTP_DETAILS", "PASSWORD"))
	smtp.sendmail(msg["From"], msg["To"].split(","), msg.as_string())
	smtp.quit()
	