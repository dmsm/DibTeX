from __future__ import print_function
from models import Assignment, Problem, Submission
import aggregator

def problem_answer_pairings(asgt):
    a_n = asgt.name
    problem_pairings = {}

    for i in range(0, asgt.problems.count()):
        name = asgt.problems[i].name
        problem_file = open(a_n + "-" + name, 'a')
        aggregator.print_header(problem_file)
        p_h = r"\begin{problem}[" + asgt.problems[i].name + "][" + asgt.problems[i].points + r"]\\"
        print(p_h, file=problem_file)
        print(asgt.problems[i].content, file=problem_file)
        print(r"\end{problem}", file=problem_file)

        solution_file = open("SOLUTIONS" + "-" + a_n + "-" + name, 'a')
        print(r"\begin{solution}", file=solution_file)
        print(asgt.problems[i].solution, file=solution_file)
        print(r"\end{solution}", file=solution_file)
        problem_pairings.append(problem_file, solution_file)

    return problem_pairings
