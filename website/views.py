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

def strip_solutions(asgt):
    problems_file = open(asgt.name + aggregator.TEX_FILE, 'a')
    aggregator.print_header(problems_file)
    print("\\name{" + asgt.name + "}", problems_file)
    print("\duedate{" + asgt.due_date + "}", problems_file)
    print("\\begin{document}", problems_file)
    for p in asgt.problems:
        prob = "\begin{problem}[" + p.name + "][" + p.points + "]\\"
        print(prob, problems_file)
        print("\end{problem}", problems_file)
        for i in range(0, 10):
            print("\\", problems_file)

    print("\end{document}",problems_file)
    return problems_file

    # def register(request):
    #     # Like before, get the request's context.
    #     context = RequestContext(request)
    #
    #     # A boolean value for telling the template whether the registration was successful.
    #     # Set to False initially. Code changes value to True when registration succeeds.
    #     registered = False
    #
    #     # If it's a HTTP POST, we're interested in processing form data.
    #     if request.method == 'POST':
    #         # Attempt to grab information from the raw form information.
    #         # Note that we make use of both UserForm and UserProfileForm.
    #         user_form = UserForm(data=request.POST)
    #         profile_form = UserProfileForm(data=request.POST)
    #
    #         # If the two forms are valid...
    #         if user_form.is_valid() and profile_form.is_valid():
    #             # Save the user's form data to the database.
    #             user = user_form.save()
    #
    #             # Now we hash the password with the set_password method.
    #             # Once hashed, we can update the user object.
    #             user.set_password(user.password)
    #             user.save()
    #
    #             # Now sort out the UserProfile instance.
    #             # Since we need to set the user attribute ourselves, we set commit=False.
    #             # This delays saving the model until we're ready to avoid integrity problems.
    #             profile = profile_form.save(commit=False)
    #             profile.user = user
    #
    #             # Now we save the UserProfile model instance.
    #             profile.save()
    #
    #             # Update our variable to tell the template registration was successful.
    #             registered = True
    #
    #         # Invalid form or forms - mistakes or something else?
    #         # Print problems to the terminal.
    #         # They'll also be shown to the user.
    #         else:
    #             print user_form.errors, profile_form.errors
    #
    #     # Not a HTTP POST, so we render our form using two ModelForm instances.
    #     # These forms will be blank, ready for user input.
    #     else:
    #         user_form = UserForm()
    #         profile_form = UserProfileForm()
    #
    #     # Render the template depending on the context.
    #     return render_to_response(
    #             'website/templates/register.html',
    #             {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
    #             context)
    #
    # def user_login(request):
    #     # Like before, obtain the context for the user's request.
    #     context = RequestContext(request)
    #
    #     # If the request is a HTTP POST, try to pull out the relevant information.
    #     if request.method == 'POST':
    #         # Gather the username and password provided by the user.
    #         # This information is obtained from the login form.
    #         username = request.POST['username']
    #         password = request.POST['password']
    #
    #         # Use Django's machinery to attempt to see if the username/password
    #         # combination is valid - a User object is returned if it is.
    #         user = authenticate(username=username, password=password)
    #
    #         # If we have a User object, the details are correct.
    #         # If None (Python's way of representing the absence of a value), no user
    #         # with matching credentials was found.
    #         if user:
    #             # Is the account active? It could have been disabled.
    #             if user.is_active:
    #                 # If the account is valid and active, we can log the user in.
    #                 # We'll send the user back to the homepage.
    #                 login(request, user)
    #                 return HttpResponseRedirect('/website/')
    #             else:
    #                 # An inactive account was used - no logging in!
    #                 return HttpResponse("Your DibTex account is disabled.")
    #         else:
    #             # Bad login details were provided. So we can't log the user in.
    #             print "Invalid login details: {0}, {1}".format(username, password)
    #             return HttpResponse("Invalid login details supplied.")
    #
    #     # The request is not a HTTP POST, so display the login form.
    #     # This scenario would most likely be a HTTP GET.
    #     else:
    #         # No context variables to pass to the template system, hence the
    #         # blank dictionary object...
    #         return render_to_response('website/login.html', {}, context)
    #
    # # Use the login_required() decorator to ensure only those logged in can access the view.
    # @login_required
    # def user_logout(request):
    #     # Since we know the user is logged in, we can now just log them out.
    #     logout(request)
    #
    #     # Take the user back to the homepage.
    #     return HttpResponseRedirect('/website/')