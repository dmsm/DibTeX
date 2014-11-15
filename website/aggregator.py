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
    print(r"\documentclass[12pt,letterpaper,boxed]{hmcpset}", file=submission_file)
    print(r"% set 1-inch margins in the document", file=submission_file)
    print(r"\usepackage[margin=1in]{geometry}", file=submission_file)
    print(r"\usepackage{marvosym}", file=submission_file)
    print(r"\usepackage{MnSymbol,wasysym}", file=submission_file)
    print(r"\usepackage{tikz}", file=submission_file)
    print(r"\usetikzlibrary{graphs,graphs.standard}", file=submission_file)
    print(r"\usepackage{color}", file=submission_file)
    print(r"\usepackage{enumerate}", file=submission_file)
    print(r"\usepackage{tikz}", file=submission_file)
    print(r"\usepackage{mathtools}", file=submission_file)
    print(r"\DeclarePairedDelimiter\ceil{\lceil}{\rceil}", file=submission_file)
    print(r"\DeclarePairedDelimiter\floor{\lfloor}{\rfloor}", file=submission_file)
    print(r"% include this if you want to import graphics files with /includegraphics", file=submission_file)

def aggregate(self, student_id, submissions):
    name = self.student_map[student_id]
    submission_file = open(name + self.assignment_name + self.TEX_FILE, 'a')
    print_header(submission_file)

    print(r"\name{" + name + "}", file=submission_file)
    print(r"\duedate{" + assignment_due_date + "}", file=submission_file)
    print(r"\begin{document}", file=submission_file)

    for submission in submissions:
        header = r"\begin{problem}[" + submission.problem.name + "]["+\
                 submission.score + "/" + submission.problem.points + r"]\\"
        print(header, file=submission_file)
        print(submission.problem.contents, file=submission_file)
        print(r"\end{problem}", file=submission_file)
        print(r'\begin{solution}', file=submission_file)
        print(submission.problem.solution, file=submission_file)
        print(r"\end{solution}", file=submission_file)

    print(r"\end{document}",file=submission_file)
