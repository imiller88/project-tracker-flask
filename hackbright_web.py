"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright as hb

app = Flask(__name__)


@app.route("/")
def index():
    """ Homepage. """

    return render_template("index.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hb.get_student_by_github(github)

    project_grades = hb.get_all_grades(github)

    html = render_template("student_info.html",
                            first=first,
                            last=last,
                            github=github,
                            project_grades=project_grades)

    return html


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    html = render_template("student_search.html")
    return html


@app.route("/student-add")
def add_student():
    """ Add a student. """

    return render_template("student_add.html")


@app.route("/student-add-success", methods=["POST"])
def return_student_success():
    print "got here"
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    github = request.form.get("github")



    hb.make_new_student(first_name, last_name, github)

    return render_template("student_add_success.html",
                            first_name=first_name,
                            last_name=last_name,
                            github=github)


@app.route("/project")
def project_listing():
    """ Returns information on project. """

    project = hb.get_project_by_title(request.args.get("project-name"))

    project_grades = hb.get_all_project_grades(project[1])

    return render_template("project_info.html", project=project, 
                        project_grades=project_grades)


if __name__ == "__main__":
    hb.connect_to_db(app)
    app.run(debug=True)
