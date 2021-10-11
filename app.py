from flask import Flask, render_template, request, redirect, flash
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
    questions_length = len(satisfaction_survey.questions)



    return render_template('questions.html', question=rendered_question, questions_len=questions_length)

@app.route("/answer", methods=["POST"])
def add_response():
    choice = request.form['answer']
    responses.append(choice)

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"questions/{len(responses)}")


@app.route("/complete")
def complete():
    return render_template("complete.html")
