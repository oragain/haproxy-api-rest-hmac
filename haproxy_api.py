#!/usr/bin/env python
from flask import Flask,request,jsonify
from hashlib import md5
import json
import socket
import hmac

tcp_ip = '127.0.0.1' # IP of the HAProxy Listener
tcp_port = 8181 # Port of the HAProxy Listener
buffer_size = 8192 # Big enough to retrieve all the data from 'HELP' maybe not from stats depending on number of backend servers
key = "ABCD-1234-EFGH-5678"
enable_hmac = True
lasttime = 0

#Sending the command passed via the API to the localhost listening IP port
def send(command):
    message = command
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((tcp_ip, tcp_port))
    s.send(message+"\n") #Add the new line character to 'execute' the command on the other side
    data = s.recv(buffer_size)
    s.close()
        #potentially add hmac validation here
    return data

def hmac_val(uri,req):
    global lasttime
    h = hmac.new(key)
    data = req.data
    time = req.headers['timestamp']
    if time < lasttime:
        return False
    else:
        lasttime = time
        signature = req.headers['signature']
        msg = uri + time + data
        h.update(msg)
        if h.hexdigest() == signature:
                return True
        else:
                return False

app = Flask(__name__)

@app.route('/hi') # Always usefull to integrate with monitoring system and know if the plug-in is responding
def hello_world():
    return 'Hello, World!'

@app.route('/send', methods=['POST'])
def set_server():
#    response = { 'header' : request.header  }
#    print request.headers
#    print request.headers['Timestamp']
#    print(request.data)
    content= request.get_json()
    if not enable_hmac or hmac_val("/send",request):
        return send(content['command']), 200
    else:
#    print response
        return "Invalid Signatures", 400

@app.errorhandler(Exception) # In case of errors, output it as the response (potential sec issue)
def exception_handler(error):
    return repr(error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)