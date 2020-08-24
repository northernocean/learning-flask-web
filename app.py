from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup_form")
def signup_form():
    return render_template("signup.html")

@app.route("/thank_you")
def thank_you():
    first = request.args.get("first")
    last = request.args.get("last")
    return render_template("thank_you.html", first=first, last=last)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

if __name__ == "__main__":
    # Alternate launch configuration for catching errors with VSCode debugger
    # https://blog.miguelgrinberg.com/post/setting-up-a-flask-application-in-visual-studio-code 
    app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)