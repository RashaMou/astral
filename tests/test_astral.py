import pytest
from astral.api import API

def test_basic_route_adding(api):
    @api.route("/home")
    def home(req, res):
        res.text = "YOLO"

    with pytest.raises(AssertionError):
        @api.route("/home")
        def home2(req, res):
            res.text = "YOLOO"

def test_astral_test_client_can_send_requests(api, client):
    RESPONSE_TEXT = "this is pretty sweet"

    @api.route("/hey")
    def sweet(req, res):
        res.text = RESPONSE_TEXT

    response = client.get("/hey")
    assert response.status_code == 200
    assert response.text == RESPONSE_TEXT

def test_parametrized_route(api, client):
    @api.route("/{name}")
    def hello(req, res, name):
        res.text = f"hey {name}"

    response = client.get("/rasha")
    assert response.status_code == 200
    assert response.text == "hey rasha"

def test_nonexistent_route(client):
    response = client.get("/boo", status=404)
    assert response.status_code == 404
    assert response.text == "No potato"

def test_class_based_handlers_get(api, client):
    RESPONSE_GET = "Books page"

    @api.route("/books")
    class BooksResource:
        def get(self, req, res):
            res.text = RESPONSE_GET

    response_get = client.get("/books")
    assert response_get.status_code == 200
    assert response_get.text == RESPONSE_GET

def test_class_based_handlers_post(api, client):
    RESPONSE_POST = "Endpoint to create a book"

    @api.route("/books")
    class BooksResource:
        def post(self, req, res):
            res.text = RESPONSE_POST

    response_post = client.post("/books")
    assert response_post.status_code == 200
    assert response_post.text == RESPONSE_POST


def test_class_based_handlers_not_allowed_method(api, client):
    @api.route("/books")
    class BooksResource:
        def post(self, req, res):
            res.text = RESPONSE_POST

    with pytest.raises(AttributeError):
        client.get("/books")
