from django.shortcuts import get_object_or_404, render, redirect as django_redirect    # Render and 404
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.models import User                         # User auth
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# Template Loader
from django.template import loader

from .link_tools import *

# Forms
from .forms import LoginForm, SignUpForm, LinkForm, ReviewForm

# Models
from .models import Link, Review, Category, UserProfile


# Create your views here.

# Link detail
# /linked/<primary_key>/
def detail(request, link_id):
    # try:
    #     link = Link.objects.get(pk=link_id)
    # except Link.DoesNotExist:
    #     raise Http404("Link does not exist!")
 


    link = get_object_or_404(Link, pk=link_id)
    if(request.method == 'POST'):       # Form Data Process If Any
        # Get the form data
        new_review_form = ReviewForm(request.POST)
        # If form is valid
        if(new_review_form.is_valid()):
            userPK = request.user.pk
            # Get fields
            print(new_review_form)
            rate = new_review_form.cleaned_data['rate']
            review = new_review_form.cleaned_data['review']
            by = UserProfile.objects.get(pk=userPK)
            # new_review = Review.objects.create(link=link, by=by, review=review, rate=rate)
            new_review.save()
            # Add user point
            # UserProfile.objects.filter(pk=userPK).update(points=F('points')+ 20)
            return django_redirect(index)

    # return HttpResponse("YOu are looking at link %s" % link.name)
    # Load template
    template = loader.get_template('linked/link.html')
    # Create context
    context = {
        'link': link,
        'auth' : request.user.is_authenticated

    }
    # return HttpResponse("type: %s" % len(links))
    # Render the template
    return HttpResponse(template.render(context, request))


# Index page
# /linked/
def index(request):
    # print(request.path[request.path.rfind('/') + 1:])
    # Retrieve links to show on the home page
    # ** Devide in categories later

    # print(":: " + request.user.bio)

    links = Link.objects.order_by('name')[:]

    final = []

    for i in range(len(links)):
        reviews = Review.objects.filter(link=links[i].pk)
        print("Reviews: " + str(len(reviews)))
        final.append(view_final_link_dict(links[i], reviews))
        # links[i]['reviews'] = reviews
        # print(links[i]['reviews'])

    # Load template
    template = loader.get_template('linked/index.html')
    # Create context
    context = {
        'links': final,
        'auth' : request.user.is_authenticated,
        'form' : ReviewForm

    }
    # return HttpResponse("type: %s" % len(links))
    # Render the template
    return HttpResponse(template.render(context, request))

# Login page
# /linked/login/


def login(request):
    form_name = "Login"                 # Form name
    if(request.method == 'POST'):       # Form Data Process If Any
        # Get the form data
        login_form = LoginForm(request.POST)
        # If form is valid
        if(login_form.is_valid()):
            # Get fields
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # Do something with the data

            # Authentocate user
            user = authenticate(request, username=username, password=password)
            # If user exists
            if(user is not None):
                # Log User In
                auth_login(request, user)
                # Load and render success page
                template = loader.get_template('linked/success.html')
                return HttpResponse(template.render({'for': 'Login'}, request))

    # Load new from
    login_form = LoginForm()
    # Load template
    template = loader.get_template('linked/form.html')
    # Cteate context
    context = {
        'form': login_form,
        'form_name': form_name,
        'auth' : request.user.is_authenticated
    }
    # Render the template
    return HttpResponse(template.render(context, request))


# Registeration page
# /linked/signup/
def signup(request):
    form_name = "Sign up"          # Form name
    if(request.method == 'POST'):       # Form Data Process If Any
        # Get the form data
        signup_form = SignUpForm(request.POST)
        # If form is valid
        if(signup_form.is_valid()):
            # Get fields
            email_address = signup_form.cleaned_data['email_address']
            password = signup_form.cleaned_data['password']
            confirm_password = signup_form.cleaned_data['confirm_password']
            username = signup_form.cleaned_data['username']
            terms_and_conditions = signup_form.cleaned_data['terms_and_conditions']

            # If passwords match and user has agreed to terms and conditions
            if(password == confirm_password and terms_and_conditions):
                # Do something with the data
                print(email_address, password, username, terms_and_conditions)
                # Create user
                user = User.objects.create_user(
                    username, email_address, password)
                # Load template
                template = loader.get_template('linked/success.html')
                # Create context
                context = {'for': 'Registration'}
                # Render the template
                return HttpResponse(template.render(context, request))

    # Load new from
    signup_form = SignUpForm()
    # Load template
    template = loader.get_template('linked/form.html')
    # Cteate context
    context = {
        'form': signup_form,
        'form_name': form_name,
        'auth' : request.user.is_authenticated
    }
    # Render the template
    return HttpResponse(template.render(context, request))


def new(request):
    form_name = "New Link"

    if(request.method == 'POST'):       # Form Data Process If Any
        # Get the form data
        new_link_form = LinkForm(request.POST)
        # If form is valid
        if(new_link_form.is_valid()):
            # Get fields
            print(new_link_form)
            link_name = new_link_form.cleaned_data['name']
            link_domain = new_link_form.cleaned_data['domain']
            link_url = new_link_form.cleaned_data['url']
            link_description = new_link_form.cleaned_data['description']
            link_category = new_link_form.cleaned_data['category']

            cat = Category.objects.get(name=link_category)

            by = UserProfile.objects.get(pk=request.user.pk)

            new_link = Link.objects.create(
                name=link_name, domain=link_domain, url=link_url, 
                description=link_description, category=cat, by=by)
            # If passwords match and user has agreed to terms and conditions
            new_link.save()
            template = loader.get_template('linked/success.html')
            # Create context
            context = {'for': 'New Link'}
            # Render the template
            return HttpResponse(template.render(context, request))

    # Load new from
    new_link_form = LinkForm()
    # Load template
    template = loader.get_template('linked/form.html')
    # Cteate context
    context = {
        'form': new_link_form,
        'form_name': form_name,
        'auth' : request.user.is_authenticated
    }
    # Render the template
    return HttpResponse(template.render(context, request))


# User profile page
# /linked/profile/
# /linked/profile/ali
def profile(request, username=None):
    # Create context with default user none
    context = {
        'user': None,
        'auth' : request.user.is_authenticated
    }

    # Load template
    template = loader.get_template('linked/profile.html')

    # If username is not set but a session exists
    if(username == None and request.user.is_authenticated):
        # Set context user to logged in user
        userProfile = UserProfile.objects.get(fk=request.user.pk)
        context['user'] = userProfile

    # If username is set
    else:
        # Fetch user specified
        user = User.objects.get(username=username)
        # userProfile = UserProfile.objects.get(user)
        # If user exists
        if(user is not None):
            # Set context user to fetched user
            context['user'] = user

    # Render the template
    return HttpResponse(template.render(context, request))


# Logout user
# /linked/logout/
def logout(request):
    # Log user out and destroy session
    auth_logout(request)
    # redirect to index
    return django_redirect(index)

# Redirect to link
# /linked/redirect/<primary_key>/


def redirect(request, link_id):
    # Get specified link if exists
    link = get_object_or_404(Link, pk=link_id)
    # Load template
    template = loader.get_template('linked/redirect.html')
    # Create contect
    context = {
        'link': link,
        'auth' : request.user.is_authenticated
    }
    # Render the template
    return HttpResponse(template.render(context, request))
