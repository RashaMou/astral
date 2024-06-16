from webob import Request, Response

class API:
    def __call__(self, environ, start_response):
        # the environ dictionary contains all the details of the incoming HTTP
        # request.
        request = Request(environ)
        response = Response()
        response.text = "Hello, world!"

        return response(environ, start_response)
