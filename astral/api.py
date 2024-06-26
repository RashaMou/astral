from parse import parse
import inspect
from webob import Request, Response
import os
from jinja2 import Environment, FileSystemLoader

class API:
    def __init__(self, templates_dir=None):
        """
        routes stores paths as keys and handlers as values
        """
        self.routes = {}

        if templates_dir is None:
            templates_dir = os.path.join(os.path.dirname(__file__), 'templates')

        self.templates_env = Environment(
            loader=FileSystemLoader(os.path.abspath(templates_dir))
        )

        self.exception_handler = None

    def __call__(self, environ, start_response):
        # the environ dictionary contains all the details of the incoming HTTP
        # request.
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def add_route(self, path, handler):
        assert path not in self.routes, f"{path} route already exists"

        self.routes[path] = handler

    def route(self, path):
        # handlers are the route functions in app.py
        def wrapper(handler):
            self.add_route(path, handler)
            return handler

        return wrapper

    def handle_request(self, request):
        response = Response()

        handler, kwargs = self.find_handler(request.path)

        try:
            if handler is not None:
                if inspect.isclass(handler):
                    handler = getattr(handler(), request.method.lower(), None)
                    if handler is None:
                        raise AttributeError("Method not allowed", request.method)
                handler(request, response, **kwargs)
            else:
                self.default_response(response)
        except Exception as e:
            if self.exception_handler is None:
                raise e
            else:
                self.exception_handler(request, response, e)

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


    def template(self, template_name, context=None):
        if context is None:
            context={}

        return self.templates_env.get_template(template_name).render(**context)

    def add_exception_handler(self, exception_handler):
        self.exception_handler = exception_handler
