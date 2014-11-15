from __future__ import print_function
from models import Assignment, Problem, Submission
import aggregator

def problem_answer_pairings(asgt):
    a_n = asgt.name
    for p in asgt.problems.all:
        name = p.name
        problem_file = open(a_n + "-" + name, 'a')
        aggregator.print_header(problem_file)
        print(p.content)
