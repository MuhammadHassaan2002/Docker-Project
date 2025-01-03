from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World from Muhammad Hassaan"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # Make sure it's accessible from outside

