from api import API

app = API()

@app.route("/home")
def home(request, response):
    response.text = "Hello from the HOME page"

@app.route("/about")
def about(request, response):
    response.text = "Hello from the ABOUT page"

@app.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"

@app.route("/tell/{age:d}")
def age(request, response, age):
    response.text = f"You are {age} years old"

@app.route("/sum/{num_1:d}/{num_2:d}")
def sum(request, response, num_1, num_2):
    sum = num_1 + num_2
    response.text = f"{num_1} + {num_2} = {sum}"

@app.route("/books")
class BooksResource:
    def get(self, req, res):
        res.text = "Books page"

    def post(self, req, res):
        res.text = "Endpoint to create a book"
