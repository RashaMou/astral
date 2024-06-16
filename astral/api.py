from webob import Request, Response

class API:
    def __call__(self, environ, start_response):
        # the environ dictionary contains all the details of the incoming HTTP
        # request.
        request = Request(environ)
        response = self.handle_request(request)

        return response(environ, start_response)

    def handle_request(self, request):
        user_agent = request.environ.get("HTTP_USER_AGENT", "No user agent found")

        response = Response()
        response.text = f"Hello friend with this user agent: {user_agent}"

        return response

