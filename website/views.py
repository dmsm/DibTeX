from __future__ import print_function
from django.shortcuts import render
from website.forms import ProfessorUploadForm
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
import re
import os
import aggregator
from website.models import Assignment, Problem, Submission
import package_problems

def professor(request):
    if request.method == 'POST':
        form = ProfessorUploadForm(request.POST, request.FILES)
        if form.is_valid():
            process_prof_file(request.FILES['file'])
            return render(request, 'profbig.html', {'form': form, 'success': "Submitted"})
    else:
        form = ProfessorUploadForm()
    return render(request, 'profbig.html', {'form': form})

def student(request):
    ass = Assignment.objects.all()

    for a in Assignment.objects.all():
        total_points = 0;
        for p in a.problems.all():
            total_points += p.points
        a.points = total_points
        a.save()

    if request.method == 'POST':
        form = ProfessorUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # process_student_file(request.FILES['file'])
            return render(request, 'index.html', {'assignments': ass, 'form': form, 'success': "Submitted"})
    else:
        form = ProfessorUploadForm()

    return render(request, "index.html", {'assignments': ass, 'form': form})

def grader(request):
    ass = Assignment.objects.all()
    list_of_list_of_problems = {}
    for a in ass:
        problems = package_problems.problem_answer_pairings(a)
        list_of_list_of_problems.append(problems)

    return render(request, "grader.html", {'problem_solution_pair_list_list': list_of_list_of_problems})


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
        o = re.search(r"([^]]*)\end{problem}", data[loc + m.end() + n.end():])
        p.contents = o.group(1)
        q = re.search(r"begin{solution}([^]]*)\\end{solution}", data[loc + m.end() + n.end() + o.end():])
        p.solution = q.group(1)
        p.save()
        asgt.problems.add(p)

    strip_solutions(asgt)
    os.system("pdflatex %s" % asgt.pk + aggregator.TEX_FILE)
    os.system("mv ./%s.pdf ./website/static/asgts/" % asgt.pk)

def strip_solutions(asgt):
    problems_file = open(str(asgt.pk) + aggregator.TEX_FILE, 'w')
    aggregator.print_header(problems_file)
    print(r"\name{" + asgt.name + "}", file=problems_file)
    print(r"\duedate{" + asgt.due_date + "}", file=problems_file)
    print(r"\begin{document}", file=problems_file)
    for p in asgt.problems.all():
        print(r"\begin{problem}[" + p.name + "][" + str(p.points) + r"]", file=problems_file)
        print(p.contents, file=problems_file)
        print(r"\end{problem}", file=problems_file)

    print(r"\end{document}",file=problems_file)
    return problems_file

def process_student_file(file):
    data = file.read()

    problem_locs = [m.end() for m in re.finditer("begin{problem}", data)]

    for loc in problem_locs:
        s = Submission()
        m = re.search(r"\[([^]]*)\]", data[loc:])
        s.name = m.group(1)
        n = re.search(r"\[([^]]*)\]", data[loc+m.end():])
        s.points = n.group(1)
        o = re.search(r"([^]]*)\end{problem}", data[loc + m.end() + n.end():])
        q = re.search(r"begin{solution}([^]]*)\\end{solution}", data[loc + m.end() + n.end() + o.end():])
        s.contents = q.group(1)
        p = Problem.objects.get(name=s.name)
        s.problem = p
        s.save()

    os.system("pdflatex %s" % asgt.pk + aggregator.TEX_FILE)
    os.system("mv ./%s.pdf ./website/static/asgts/" % asgt.pk)
