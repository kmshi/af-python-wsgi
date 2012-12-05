#import bottle
#import os

#def application(environ, start_response):
#    data = "Hello World! AppFog Python Support"
#    start_response("200 OK", [
#            ("Content-Type", "text/plain"),
#            ("Content-Length", str(len(data)))
#            ])
#    return iter([data])

from bottle import route, run, debug, template, request, validate, static_file, error

# only needed when you run Bottle on mod_wsgi
from bottle import default_app

@route('/hello/:name')
def index(name='World'):
    return template('<b>Hello {{name}}</b>!', name=name)

@error(403)
def mistake403(code):
    return 'There is a mistake in your url!'

@error(404)
def mistake404(code):
    return 'Sorry, this page does not exist!'

application = default_app()

