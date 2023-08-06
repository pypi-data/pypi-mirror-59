# python-logware
## RequestLogger  
Request logging middleware for python web services. Use this library to log the requests hitting the web service. It is advised to use **Request-Id** in request headers to trace the spread of requests in microservice environment.

**Package library:** [logware](https://pypi.org/project/logware/)  
**Stable Version:** 0.1.1  
**Supported python versions:** 2.7 and 3.6+  
**Supported python web frameworks:** [Bottle](https://bottlepy.org/)

## How to install?
run `pip install logware`

## How to use?
```python
import bottle
from logware import RequestLogger

app = bottle.app()
myapp = RequestLogger(app,log_level="ERROR",service_name="TEST")

@bottle.route('/hello')
def hello():
    return "Hello World!"

@bottle.route('/bad')
def bad():
    return bottle.HTTPResponse(status=400, body={"message": "bad request"})
bottle.run(app=myapp)
```

### Parameters
app: instance of bottle application
log_level: only INFO or ERROR is supported, defaults to INFO
service_name: Name of the service, defaults to empty string.

### Initialising without config
```python
app = bottle.app()
myapp = RequestLogger(app,log_level="ERROR",service_name="TEST")
```
Sets the __log level__ to __error__, logs only the failed requests.

### Initialising without config
```python
app = bottle.app()
myapp = RequestLogger(app)
```
Sets the __log level__ to __info__, logs all the requests.

### Log example:
The log prints in json string format.  
```{"level":"error","service":"test","message":"{\"message\": \"bad request\"}","uri":"/bad?a=1","responseCode":400,"requestId":"23545"}```
