from __future__ import print_function
from models import Assignment, Problem, Submission

student_map = {}
assignment_name = ""
assignment_due_date = ""
TEX_FILE = ".tex"

def set_assignment_name(self, name):
    self.assignment_name = name

def set_due_date(self, due_date):
    self.assignment_due_date = due_date

def create_id_map(self, student_id, student_name):
    self.student_map[student_id] = student_name

def print_header(submission_file):
    print("\documentclass[12pt,letterpaper,boxed]{hmcpset}", file=submission_file)
    print("% set 1-inch margins in the document", file=submission_file)
    print("\usepackage[margin=1in]{geometry}", file=submission_file)
    print("\usepackage{marvosym}", file=submission_file)
    print("\usepackage{MnSymbol,wasysym}", file=submission_file)
    print("\usepackage{tikz}", file=submission_file)
    print("\usetikzlibrary{graphs,graphs.standard}", file=submission_file)
    print("\usepackage{color}", file=submission_file)
    print("\usepackage{enumerate}", file=submission_file)
    print("\usepackage{tikz}", file=submission_file)
    print("\usepackage{mathtools}", file=submission_file)
    print("\DeclarePairedDelimiter\ceil{\lceil}{\\rceil}", file=submission_file)
    print("\DeclarePairedDelimiter\\floor{\\lfloor}{\\rfloor}", file=submission_file)
    print("% include this if you want to import graphics files with /includegraphics", file=submission_file)

def aggregate(self, student_id, submissions):
    name = self.student_map[student_id]
    submission_file = open(name + self.assignment_name + self.TEX_FILE, 'a')
    print_header(submission_file)

    print("\\name{" + name + "}", file=submission_file)
    print("\duedate{" + assignment_due_date + "}", file=submission_file)
    print("\\begin{document}", file=submission_file)

    for submission in submissions:
        header = "\\begin{problem}[" + submission.problem.name + "]["+\
                 submission.score + "/" + submission.problem.points + "]\\"
        print(header, file=submission_file)
        print(submission.problem.contents, file=submission_file)
        print("\end{problem}", file=submission_file)
        print("\\begin{solution}", file=submission_file)
        print(submission.problem.solution, file=submission_file)
        print("\end{solution}", file=submission_file)

    print("\end{document}",file=submission_file)
