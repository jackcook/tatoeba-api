from flask import Flask

app = Flask(__name__)

@app.route("/contributions")
def contributions():
    return "Hello world"

if __name__ == "__main__":
    app.run(debug=True)