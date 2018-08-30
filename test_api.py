#!/usr/bin/env python
from textwrap import dedent
from hashlib import md5
import json
import os
import socket
import hmac
import httplib, urllib
import requests


data = {"command":"show stat"}
timestamp = "2018-05-16Z13:22:00"
key = "ABCD-1234-EFGH-5678"
uri = "/send"

h = hmac.new(key)
msg = uri + timestamp + json.dumps(data)
print(msg)
h.update(msg)
signature = h.hexdigest()
print(signature)

h_ts = "timestamp: "+timestamp
h_sig = "signature: "+signature

headers = {"Content-type": "application/json",
    "Accept": "text/plain",
    "timestamp" : timestamp,
    "signature" : signature
}

url = "http://haproxy:5000"+uri

r = requests.post(url, data=json.dumps(data), headers=headers)
print (r.content)