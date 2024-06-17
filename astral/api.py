from parse import parse
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
        if path in self.routes.keys():
            raise AssertionError(f"{path} route already exists")
        # handlers are the route functions in app.py
        def wrapper(handler):
            self.routes[path] = handler
            return handler

        return wrapper

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request.path)

        if handler is not None:
            handler(request, response, **kwargs)
        else:
            self.default_response(response)

        return response

    def find_handler(self, req_path):
        for path, handler in self.routes.items():
            parse_result = parse(path, req_path)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def default_response(self, response):
        response.status_code = 404
        response.text = "No potato"
