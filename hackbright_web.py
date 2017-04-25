"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright as hb

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hb.get_student_by_github(github)

    html = render_template("student_info.html",
                            first=first,
                            last=last,
                            github=github)

    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    html = render_template("student_search.html")
    return html


if __name__ == "__main__":
    hb.connect_to_db(app)
    app.run(debug=True)
