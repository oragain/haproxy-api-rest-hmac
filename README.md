# Python simple API to pipe commands to HAProxy via REST with HMAC Authentication
## Introduction
I built this mini API to add a layer of security when issuing remote commands to a community HAProxy service.
This API is a pipe straight into HAProxy tcp listener with an added security layer in the form of HMAC and timestamp authentication. 
It runs on the HAProxy load balancers and HAProxy tcp listener must be enabled. To disable remote connectivity, bound the HAProxy listener to 127.0.0.1.

Current bugs:
* In case of a restart of the Python API, the timestamp validation is reset.
* Bugger contains 8192 Bytes at most, so for big configuration, it may need to be increased fixed.

Potential improvements:
* Modify to pipe to vamp community or alternate haproxy-api interfaces not offering an authentication layer

## Files
### haproxy_api.py
The API code. Modify it to change the ip / ports for the HAProxy TCP listener

### test_api.py
A mini script to test the api remotely or locally

### haproxy_api.service
A service file that can be used to create an haproxy_api service. Modify the paths to the haproxy_api.py file location and the running user.

## Copyright
All licenses in this repository are copyrighted by their respective authors.
Everything else is released under GNU. See `LICENSE` for details.
