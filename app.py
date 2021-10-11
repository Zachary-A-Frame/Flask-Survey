from flask import Flask, render_template, request
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)

responses = []

@app.route("/")
def generate_home():
    """Generate Survey Title and Instructions."""

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("home.html", title=title, instructions=instructions)

@app.route("/questions/<int:question_id>")
def render_questions(question_id):

    rendered_question = satisfaction_survey.questions[question_id]

    return render_template('questions.html', question=rendered_question)
