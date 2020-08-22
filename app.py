from flask import Flask
app = Flask(__main__)

@app.route("/")
def index():
    return "<h1>Hello World!</h1>"

if __name__ == "__main__":
    app.run()
