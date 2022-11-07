from flask import Flask

app = Flask(__name__)
app.config.from_pyfile('/path/to/file.cfg')

@app.route("/")
def hello():
    return "hello world!"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
