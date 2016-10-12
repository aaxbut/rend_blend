import urllib2
import json

json_payload = json.dumps({'a':1})
headers = {'Content-Type':'application/json; charset=utf-8'}
req = urllib2.Request('http://127.0.0.1:781/tr', json_payload, headers)
resp = urllib2.urlopen(req)