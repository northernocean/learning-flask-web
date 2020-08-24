from flask import Flask

app = Flask(__name__)

app.config["SECRET_KEY"] = "butter-candy-rocks"


@app.route("/")
def index():
    return render_template("index.html")