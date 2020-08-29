from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField, BooleanField, DateTimeField, 
    RadioField, SelectField, TextField, TextAreaField, SubmitField)
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config["SECRET_KEY"] = "butter-candy-maple"


class MyForm(FlaskForm):

    breed = StringField("What breed are you?", validators=[DataRequired()])
    neutered = BooleanField("Have you been neutered?")
    mood = RadioField("Please choose your mood:", choices=[("1","happy"), ("2","hungry"), ("3", "excited")])
    food_choice = SelectField("Pick your favorite food: ", choices=[("c","chicken"), ("b","beef"), ("f","fish")])
    feedback = TextAreaField("Your Feedback:")
    submit = SubmitField("Submit")


@app.route("/", methods=["GET","POST"])
def index():

    form = MyForm()
    
    if form.validate_on_submit():
        session["breed"] = form.breed.data
        session["neutered"] = form.neutered.data
        session["mood"] = form.mood.data
        session["food_choice"] = form.food_choice.data
        session["feedback"] = form.feedback.data
    
        return redirect(url_for("thank_you"))
    
    return render_template("index.html", form=form)


@app.route("/thank_you")
def thank_you():
    return render_template("thank_you.html")
