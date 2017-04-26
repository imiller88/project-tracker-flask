"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """ #execute only pulls parameters preceded by :
    db_cursor = db.session.execute(QUERY, {'github': github}) #'github' = :github
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (row[0], row[1], row[2])
    return row


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    QUERY = """
        INSERT INTO students
        VALUES (:first_name, :last_name, :github)"""

    db.session.execute(QUERY, {'first_name': first_name,
                                'last_name': last_name,
                                'github': github})

    db.session.commit()

    # return first_name, last_name, github
    print "Successfully added student: %s %s with github %s" % (first_name,
                                                                last_name, github)


def get_project_by_title(title):
    """Given a project title, print information about the project."""

    QUERY = """
        SELECT *
        FROM projects
        WHERE title = :title """

    db_cursor = db.session.execute(QUERY, {'title': title})
    row = db_cursor.fetchone()

    # print "Project %s: %s\nMax grade: %s" % (row[1], row[2], row[3])
    return row


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    QUERY = """ 
        SELECT *
        FROM grades
        WHERE project_title = :title AND student_github = :github """

    db_cursor = db.session.execute(QUERY, {'title': title,
                                            'github': github})
    row = db_cursor.fetchone()

    print "Student %s received a grade of %s on project %s." % (row[1], 
                                                                row[3], row[2])
    return row

def get_all_project_grades(title):
    """ For a given project, list all students and grades. """
    
    QUERY = """ 
        SELECT students.first_name, students.last_name, grades.grade, students.github 
        FROM grades JOIN students ON (students.github = grades.student_github)
        WHERE project_title = :title
        """
    db_cursor = db.session.execute(QUERY, {'title': title})

    rows = db_cursor.fetchall()

    return rows


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    
    QUERY = """
        UPDATE grades
        SET grade = :grade
        WHERE student_github = :github AND project_title = :title """

    db.session.execute(QUERY, {'github': github,
                                'title': title,
                                'grade': grade})

    db.session.commit()

    print "Successfully updated %s's grade on project %s to %s" % (github, title, grade)


def add_project(title, description, max_grade):
    """ Adds a project to the projects table. """

    QUERY = """
        INSERT INTO projects (title, description, max_grade)
        VALUES (:title, :description, :max_grade) """

    db.session.execute(QUERY, {'title': title,
                                'description': description,
                                'max_grade': max_grade})
    db.session.commit()

    print "Successfully added project %s: %s, with max grade %s." % (title, description, max_grade)


def get_all_grades(github):
    """ Get all project grades for a given student. """

    QUERY = """
        SELECT *
        FROM grades
        WHERE student_github = :github """

    db_cursor = db.session.execute(QUERY, {'github': github})

    rows = db_cursor.fetchall()

    if not rows:
        print "Sorry, that student github does not exist in the DB."
    else:
        # for row in rows:
        #     print "Student %s completed project %s and received a grade of %s." % (row[1], row[2], row[3])
        
        return rows


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command. Command and arguments must all be separated by a double space."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split("  ")
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project_info":
            title = args[0]
            get_project_by_title(title)

        elif command == "get_grade":
            github, title = args
            get_grade_by_github_title(github, title)

        elif command == "assign_grade":
            github, title, grade = args
            assign_grade(github, title, grade)

        elif command == "add_project":
            title, description, max_grade = args
            add_project(title, description, max_grade)

        elif command == "get_all_grades":
            github = args[0]
            get_all_grades(github)

        else:
            if command != "quit":
                print "Invalid Entry. Try again."

if __name__ == "__main__":
    app = Flask(__name__)
    connect_to_db(app)

    handle_input()

    db.session.close()
