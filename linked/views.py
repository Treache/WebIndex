from django.shortcuts import get_object_or_404, render, redirect as django_redirect  # Render and 404
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.models import User  # User auth
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# Template Loader
from django.template import loader
from django.db.models import Q

from django.db.models import Avg
from .link_tools import *
from .linked_config import requirements as pointreq, points as rewards

# Forms
from .forms import LoginForm, SignUpForm, LinkForm, ReviewForm, UserProfileForm, CategoryForm

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
    if request.method == 'POST':  # Form Data Process If Any
        # Get the form data
        new_review_form = ReviewForm(request.POST)
        # If form is valid
        if new_review_form.is_valid():
            userpk = request.user.pk
            # Get fields
            rate = new_review_form.cleaned_data['rate']
            review = new_review_form.cleaned_data['review']
            by = UserProfile.objects.get(pk=userpk)
            new_review = Review(link=link, by=by, review=review, rate=rate)
            new_review.save()
            # Add user point
            # UserProfile.objects.filter(pk=userPK).update(points=F('points')+ 20)
            by.addPoints(rewards['review'])
            return django_redirect(index)

    # return HttpResponse("YOu are looking at link %s" % link.name)
    # Load template
    template = loader.get_template('linked/link.html')
    # Create context
    context = {
        'link': link,
        'auth': request.user.is_authenticated

    }
    # return HttpResponse("type: %s" % len(links))
    # Render the template
    return HttpResponse(template.render(context, request))


# Index page
# /linked/
def index(request):
    # print(request.path[request.path.rfind('/') + 1:])
    # Retrieve links to show on the home page
    # ** Divide in categories later

    # print(":: " + request.user.bio)

    categories = Category.objects.order_by('created_on')[:]

    the_final_retrieved = []

    for category in categories:
        the_dict = {'category': category, 'links': []}
        links = Link.objects.filter(category__id=category.pk)
        for link in links:
            reviews = Review.objects.filter(link=link.pk)
            avg = reviews.aggregate(Avg('rate'))
            total = reviews.count()
            the_dict['links'].append(final_link_review_calc_dict(link, reviews, avg, total))

        the_final_retrieved.append(the_dict)
        print("==================================")
        print(the_final_retrieved[0]['links'][0])

        for cat in the_final_retrieved:
            print("CAT: " + str(cat['category']))
            for link in cat['links']:
                print(link)


    # Load template
    template = loader.get_template('linked/index.html')
    # Create context
    context = {
        'cats': the_final_retrieved,
        'auth': request.user.is_authenticated,
        'form': ReviewForm

    }
    # return HttpResponse("type: %s" % len(links))
    # Render the template
    return HttpResponse(template.render(context, request))


# Login page
# /linked/login/


def login(request):
    form_name = "Login"  # Form name
    if (request.method == 'POST'):  # Form Data Process If Any
        # Get the form data
        login_form = LoginForm(request.POST)
        # If form is valid
        if (login_form.is_valid()):
            # Get fields
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            # Do something with the data

            print("HERE " + username + " " + password)
            # Authentocate user
            user = authenticate(request, username=username, password=password)
            # If user exists
            if (user is not None):
                print("HERE " + username + " " + password)
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
        'auth': request.user.is_authenticated
    }
    # Render the template
    return HttpResponse(template.render(context, request))


# Registeration page
# /linked/signup/
def signup(request):
    # form_ext
    form_name = "Sign up"  # Form name
    print("a")
    if (request.method == 'POST'):  # Form Data Process If Any
        print("b")
        # Get the form data
        signup_form = SignUpForm(request.POST)
        user_profile_form = UserProfileForm(request.POST)
        # If form is valid
        print("c")
        print("signup is valid " + str(signup_form.is_valid()))
        print("upf is valid " + str(user_profile_form.is_valid()))
        if (signup_form.is_valid() and user_profile_form.is_valid()):
            print("d")
            # Get User Fields
            email_address = signup_form.cleaned_data['email_address']
            password = signup_form.cleaned_data['password1']
            confirm_password = signup_form.cleaned_data['password2']
            username = signup_form.cleaned_data['username']

            # Get Profile Fields
            display_name = user_profile_form.cleaned_data['display_name']
            bio = user_profile_form.cleaned_data['bio']
            terms_and_conditions = user_profile_form.cleaned_data['terms_and_conditions']
            print("e")

            # If passwords match and user has agreed to terms and conditions
            if (password == confirm_password and terms_and_conditions):
                print("f")
                # Do something with the data
                print(email_address, password, username, terms_and_conditions)
                print("a")
                # Create user
                user = User.objects.create_user(
                    username=username, email=email_address, password=password)
                # user.save()

                user_profile = UserProfile(user=user, display_name=display_name, bio=bio,
                                           terms_and_conditions=terms_and_conditions)

                user_profile.save()

                # Load template
                template = loader.get_template('linked/success.html')
                # Create context
                context = {'for': 'Registration'}
                # Render the template
                return HttpResponse(template.render(context, request))
            else:
                print("NOT SAME")

    # Load new froms
    signup_form = SignUpForm()
    user_profile_form = UserProfileForm()
    # Load template
    template = loader.get_template('linked/form.html')
    # Cteate context
    context = {
        'form': signup_form,
        'profile': user_profile_form,
        'form_name': form_name,
        'auth': request.user.is_authenticated
    }
    # Render the template
    return HttpResponse(template.render(context, request))


def new(request):
    form_name = "New Link"

    if (request.method == 'POST'):  # Form Data Process If Any
        # Get the form data
        new_link_form = LinkForm(request.POST)
        # If form is valid
        if (new_link_form.is_valid()):
            # Get fields
            print(new_link_form)
            link_name = new_link_form.cleaned_data['name']
            link_domain = new_link_form.cleaned_data['domain']
            link_url = new_link_form.cleaned_data['url']
            link_description = new_link_form.cleaned_data['description']
            link_category = new_link_form.cleaned_data['category']

            cat = Category.objects.get(name=link_category)

            by = UserProfile.objects.get(user=request.user)

            new_link = Link.objects.create(
                name=link_name, domain=link_domain, url=link_url,
                description=link_description, category=cat, by=by)
            # If passwords match and user has agreed to terms and conditions
            new_link.save()
            by.addPoints(rewards['add'])
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
        'auth': request.user.is_authenticated
    }
    # Render the template
    return HttpResponse(template.render(context, request))


def new_category(request):
    form_name = "New Category"
    print("HERE")
    user_profile = UserProfile.objects.get(user__pk=request.user.pk)
    if (not request.user.is_authenticated or user_profile.points < pointreq['new_category']):
        return django_redirect(index)

    if (request.method == 'POST'):
        new_category_form = CategoryForm(request.POST)
        if (new_category_form.is_valid()):
            category = Category(name=new_category_form.cleaned_data['name'], created_by=user_profile)
            category.save()
            template = loader.get_template('linked/success.html')
            # Create context
            context = {'for': 'New Category'}
            # Render the template
            return HttpResponse(template.render(context, request))

    # Load category form
    new_category_form = CategoryForm()
    # Load template
    template = loader.get_template('linked/form.html')
    # Create context
    context = {
        'form': new_category_form,
        'form_name': form_name,
        'auth': request.user.is_authenticated
    }

    return HttpResponse(template.render(context, request))


# User profile page
# /linked/profile/
# /linked/profile/ali
def profile(request, username=None):
    # Create context with default user none
    context = {
        'user': None,
        'auth': request.user.is_authenticated
    }

    # Load template
    template = loader.get_template('linked/profile.html')

    # If username is not set but a session exists
    if (username == None and request.user.is_authenticated):
        # Set context user to logged in user
        userProfile = UserProfile.objects.get(user__pk=request.user.pk)
        print(userProfile)
        context['user'] = userProfile

    # If username is set
    else:
        # Fetch user specified
        user = User.objects.get(username=username)
        # userProfile = UserProfile.objects.get(user)
        # If user exists
        if (user is not None):
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
        'auth': request.user.is_authenticated
    }
    # Render the template
    return HttpResponse(template.render(context, request))
