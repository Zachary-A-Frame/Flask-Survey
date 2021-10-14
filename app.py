# complete

from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "secret"

debug = DebugToolbarExtension(app)
RESPONSES_KEY = "responses"
# responses = []


@app.route("/")
def generate_home():
    """Generate Survey Title and Instructions."""

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template("home.html", title=title, instructions=instructions)


@app.route("/begin", methods=["POST"])
def begin():
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")


@app.route("/questions/<int:question_id>")
def render_questions(question_id):

    rendered_question = satisfaction_survey.questions[question_id]
    questions_length = len(satisfaction_survey.questions)

    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        # trying to access question page too soon
        return redirect("/")

    if (len(responses) == len(satisfaction_survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")

    if (len(responses) != question_id):
        # Trying to access questions out of order.
        flash(f"Invalid question id: {question_id}.")
        return redirect(f"/questions/{len(responses)}")

    return render_template('questions.html', question=rendered_question, questions_len=questions_length)

@app.route("/answer", methods=["POST"])
def add_response():
    choice = request.form['answer']
    # responses.append(choice)

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"questions/{len(responses)}")


@app.route("/complete")
def complete():
    return render_template("complete.html")
