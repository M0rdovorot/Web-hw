from urllib.parse import parse_qs
from cgi import parse


def application(environ, start_response):
    print(environ)
    # print(start_response)
    if environ['REQUEST_METHOD'] == 'POST':
        params = parse_qs(environ['wsgi.input'].read())
        print(params)
    elif environ['REQUEST_METHOD'] == 'GET':
        params = parse_qs(environ['QUERY_STRING'])
        print(params)
    start_response('200 OK', [('Content-type', 'text/html'),])
    return [str.encode(str(params)+'\n')]
