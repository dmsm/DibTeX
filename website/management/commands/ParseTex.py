from django.core.management.base import BaseCommand, CommandError
from website.models import Assignment, Problem
import re

class Command(BaseCommand):

    def handle(self, *args, **options):
        file = open("sample.tex", "r")
        data = file.read()

        m = re.search(r"assignment{(.*)}", data)
        name = m.group(1)

        m = re.search(r"duedate{(.*)}", data)
        due_date = m.group(1)

        asgt = Assignment(name=name, due_date=due_date)
        asgt.save()


        problem_locs = [m.end() for m in re.finditer("begin{problem}", data)]

        for loc in problem_locs:
            p = Problem()
            m = re.search(r"\[([^]]*)\]", data[loc:])
            p.name = m.group(1)
            n = re.search(r"\[([^]]*)\]", data[loc+m.end():])
            p.points = n.group(1)
            o = re.search(r"([^]]*)\\end{problem}", data[loc + m.end() + n.end():])
            p.contents = o.group(1)
            q = re.search(r"begin{solution}([^]]*)\\end{solution}", data[loc + m.end() + n.end() + o.end():])
            p.solution = q.group(1)
            p.save()
            asgt.problems.add(p)
        self.stdout.write("ok")