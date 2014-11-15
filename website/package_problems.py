from __future__ import print_function
from models import Assignment, Problem, Submission
import aggregator

def problem_answer_pairings(asgt):
    a_n = asgt.name
    problem_pairings = {}
    for p in asgt.problems.all:
        name = p.name
        problem_file = open(a_n + "-" + name, 'a')
        aggregator.print_header(problem_file)
        p_h = r"\begin{problem}[" + p.name + "][" + p.points + r"]\\"
        print(p_h, file=problem_file)
        print(p.content, file=problem_file)
        print(r"\end{problem}", file=problem_file)
        problem_pairings.append(problem_file)

    return problem_pairings
