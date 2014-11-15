from __future__ import print_function
from models import Assignment, Problem, Submission
import aggregator
import os



def problem_solution_file(problem):
    problem_file = open("p"+str(problem.pk) + aggregator.TEX_FILE, 'w')
    aggregator.print_header(problem_file)
    print(r"\begin{document}",file=problem_file)
    p_h = r"\begin{problem}[" + problem.name + "][" + str(problem.points) + r"]\\"
    print(p_h, file=problem_file)
    print(problem.contents, file=problem_file)
    print(r"\end{problem}", file=problem_file)
    print(r"\begin{solution}", file=problem_file)
    print(problem.solution, file=problem_file)
    print(r"\end{solution}", file=problem_file)
    print(r"\end{document}",file=problem_file)
    print("pdflatex %s" % "p"+str(problem.pk) + aggregator.TEX_FILE)
    problem_file.close()
    os.system("pdflatex %s" % "p"+str(problem.pk) + aggregator.TEX_FILE)
    os.system("mv p%s.pdf ./website/static/probs/" % problem.pk)


def submission_files(submission):
    submission_file = open("s"+str(submission.pk) + aggregator.TEX_FILE, 'w')
    aggregator.print_header(submission_file)
    print(r"\begin{document}",file=submission_file)
    print(r"\begin{solution}", file=submission_file)
    print(submission.contents, file=submission_file)
    print(r"\end{solution}", file=submission_file)
    print(r"\end{document}",file=submission_file)
    submission_file.close()
    os.system("pdflatex %s" % "s"+str(submission.pk) + aggregator.TEX_FILE)
    os.system("mv s%s.pdf ./website/static/subs/" % submission.pk)