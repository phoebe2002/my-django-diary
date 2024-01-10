# your_app/views.py

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm
from .models import EmailConfirmation
from .models import DiaryEntry
# from django.utils import timezone

def index(request):
    return render(request,'entry/index.html')

def login_prompt(request):
    return render(request, 'entry/login_prompt.html')

def home(request):
    # Retrieve recent diary entries (customize this query based on your model)
    recent_entries = DiaryEntry.objects.all()[:5]

    return render(request, 'entry/home.html', {'recent_entries': recent_entries})

def add_entry(request):
    current_datetime = timezone.now()
    return render(request, 'entry/add_entry.html', {'current_datetime': current_datetime})


def send_confirmation_email(request, user):
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    message = render_to_string('activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(subject, message, to=[to_email])
    email.content_subtype = 'html'
    email.send()

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # User is not active until email is confirmed
            user.save()

            # Send confirmation email
            send_confirmation_email(request, user)

            return render(request, 'registration_success.html')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with your desired home view
            else:
                error_message = "Invalid username or password. Please try again."
                return render(request, 'entry/login_prompt.html', {'error_message': error_message})
    form = AuthenticationForm()
    return render(request, 'entry/login_prompt.html', {'form': form})

@login_required
def restricted_view(request):
    return render(request, 'restricted.html')

def save_entry_view(request):
    if request.method == 'POST':
        # Retrieve form data from the POST request
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Create a new DiaryEntry object and save it to the database
        new_entry = DiaryEntry(title=title, content=content)
        new_entry.save()

        # Redirect to a success page or any other page
        return redirect('success_page')  # Replace 'success_page' with your desired success page URL pattern

    # If the request method is not POST, render the form again or redirect to another page
    return redirect('another_page')  # Replace 'another_page' with your desired page URL patter

# from django.shortcuts import render
# from django.contrib.auth import get_user_model
# from django.shortcuts import render, redirect
# from django.utils.crypto import get_random_string
# from django.shortcuts import get_object_or_404, redirect

# from .models import EmailConfirmation
# from .utils import send_confirmation_email
#
# # Create your views here.
#

#

#
# def register(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#
#         # Create a user without saving to the database
#         user = get_user_model()(username=username, email=email)
#         user.set_password(password)
#         user.save()
#
#         # Generate a unique token
#         token = get_random_string(length=32)
#
#         # Create an EmailConfirmation record
#         confirmation = EmailConfirmation(user=user, token=token)
#         confirmation.save()
#
#         # Send confirmation email (implement this function)
#         send_confirmation_email(user.email, token)
#
#         return redirect('registration_success')  # Redirect to a success page
#
#     return render(request, 'registration.html')
#
def confirm_email(request, token):
    confirmation = get_object_or_404(EmailConfirmation, token=token)

    # Check if the confirmation link is still valid (e.g., within 24 hours)
    if timezone.now() - confirmation.created_at > timezone.timedelta(hours=24):
        # Token has expired, handle accordingly (e.g., show an error message)
        return render(request, 'confirmation_expired.html')

    # Activate the user's account
    user = confirmation.user
    user.is_active = True
    user.save()

    # send email confirmation
    send_confirmation_email(user.email, token)

    # Delete the confirmation record
    confirmation.delete()

    return redirect('registration_success')
    # return render(request, 'confirmation_success.html')
#
# # def send_confirmation_email(request, user):
# #     current_site = get_current_site(request)
# #     protocol = 'https' if request.is_secure() else 'http'
# #     subject = 'Activate Your Account'
# #     message = render_to_string('registration_email.html', {
# #         'user': user,
# #         'protocol': protocol,
# #         'domain': current_site.domain,
# #         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
# #         'token': token_generator.make_token(user),
# #     })
# #     to_email = form.cleaned_data['email']
# #     email = EmailMessage(subject, message, to=[to_email])
# #     email.content_subtype = 'html'
# #     email.send()