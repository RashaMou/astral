from webob import Request, Response

class API:
    def __init__(self):
        """
        routes stores paths as keys and handlers as values
        """
        self.routes = {}

    def __call__(self, environ, start_response):
        # the environ dictionary contains all the details of the incoming HTTP
        # request.
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def route(self, path):
        # handlers are the route functions in app.py
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def handle_request(self, request):
        response = Response()

        for path, handler in self.routes.items():
            if path == request.path:
                handler(request, response)
                return response

        self.default_response(response)
        return response

    def default_response(self, response):
        response.status_code = 404
        response.text = "No potato"
