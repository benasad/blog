import requests
import os
import json
from requests.packages.urllib3.exceptions import SubjectAltNameWarning
requests.packages.urllib3.disable_warnings(SubjectAltNameWarning)
installloc = os.getcwd() + "/"

def authenticate():
	#Get login token
	r = requests.get('https://esm:8443/www/core-service/rest/LoginService/login?login=api&password=password&alt=json', verify=installloc+'esm.crt')
	values = r.json()
        authToken = values['log.loginResponse']['log.return']
	return authToken

def logout(authToken):
	r = requests.get('https://esm:8443/www/core-service/rest/LoginService/logout?authToken='+authToken+'&alt=json', verify=installloc+'esm.crt')

def getEntries(authToken, resourceId):
	jsoninput="""{
	"act.getEntries" : {
	"act.authToken" : '"""+ authToken +"""',
	"act.resourceId" : '""" + resourceId + """'
	}
	}"""
	headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
	print jsoninput
        r = requests.post('https://esm:8443/www/manager-service/rest/ActiveListService/getEntries', verify=installloc+'esm.crt', data=jsoninput, headers=headers)
        values = r.json()
        return values['act.getEntriesResponse']['act.return']['entryList']

authToken = authenticate()

entries = getEntries(authToken, "HRGaky2ABABCL9M8amUoLtg==")

line = ""
for entry in entries:
    for field in entry['entry']:
        line += str(field)
        line += ","
    print line.rstrip(',')
    line = ""

logout(authToken)

