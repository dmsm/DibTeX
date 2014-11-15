from __future__ import print_function
from django.shortcuts import render
from website.forms import ProfessorUploadForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
import re
import aggregator
from website.models import Assignment, Problem

def professor(request):
    if request.method == 'POST':
        form = ProfessorUploadForm(request.POST, request.FILES)
        if form.is_valid():
            process_prof_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = ProfessorUploadForm()
    return render(request, 'profbig.html', {'form': form})

def student(request):
    ass = Assignment.objects.all()

    for a in Assignment.objects.all():
        total_points = 0;
        for p in a.problems:
            total_points += p.points
        a.points = total_points

    return render(request, "index.html", {'assignments': ass})


def process_prof_file(file):
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

    strip_solutions(asgt)

def strip_solutions(asgt):
    problems_file = open(asgt.name + aggregator.TEX_FILE, 'w')
    aggregator.print_header(problems_file)
    print(r"\\name{" + asgt.name + "}", file=problems_file)
    print(r"\duedate{" + asgt.due_date + "}", file=problems_file)
    print(r"\\begin{document}", file=problems_file)
    for p in asgt.problems.all():
        print(r"\begin{problem}[" + p.name + "][" + str(p.points) + r"]", file=problems_file)
        print(p.contents, file=problems_file)
        print(r"\end{problem}", file=problems_file)

    print(r"\end{document}",file=problems_file)
    return problems_file
