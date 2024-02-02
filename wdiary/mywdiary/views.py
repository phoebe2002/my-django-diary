# your_app/views.py

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.http import HttpResponse
from lxml import etree

from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView
from .forms import SignUpForm
from .models import EmailConfirmation
from .models import DiaryEntry, CustomUser
from .forms import DiaryEntryForm, PasswordResetForm
from .forms import UserLoginForm
from django.contrib import messages
import xml.etree.ElementTree as ET
from django.core.mail import send_mail
from django.urls import reverse


# from django.utils import timezone


def index(request):
    print("we are on signup page")

    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            print("Form is valid. Proceeding with user creation.")
            user = form.save()
            user.save()

            # Send confirmation email
            email = form.cleaned_data.get('email')
            print(f"Email from form: {email}")
            send_confirmation_email(email, user, request)

            return redirect('confirmation_sent')
        else:
            print("Form is not valid. Errors:", form.errors)
            print("Form data attempt:", request.POST)
    else:
        form = SignUpForm()

    return render(request, 'entry/index.html', {'form': form})


def home(request):
    # Retrieve recent diary entries (customize this query based on your model)
    recent_entries = DiaryEntry.objects.all()[:5]

    return render(request, 'entry/home.html', {'recent_entries': recent_entries})


def save_entry_view(request):
    form = DiaryEntryForm(request.POST)
    if request.method == 'POST':
        # form = DiaryEntryForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            return redirect('home')  # Replace 'home' with your home URL name or pattern

    # If form is not valid or method is not POST, return to add_entry page with the form
    return render(request, 'entry/add_entry.html', {'form': form})


def save_entry_view(request, entry_id=None):
    # If entry_id is provided, retrieve the existing entry for modification
    if entry_id:
        entry = get_object_or_404(DiaryEntry, id=entry_id)
        user = entry.user if hasattr(entry, 'user') else request.user
    else:
        entry = None
        user = request.user

    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, instance=entry)

        # Check the value of the "action" parameter
        if form.is_valid():
            action = request.POST.get('action')

            if action == 'save_entry':
                # Save a new entry
                form.save(user)
            elif action == 'save_modifications':
                # Update the existing entry
                form.save()

            return redirect('home')  # Replace 'home' with your desired home URL name or pattern

    else:
        form = DiaryEntryForm(instance=entry)

    return render(request, 'entry/add_entry.html', {'form': form, 'entry_id': entry_id})



def send_confirmation_email(email, user, request):
    print(f"Sending confirmation email to: {email}")
    current_site = get_current_site(request)
    subject = 'Activate Your Account'
    message = render_to_string('entry/activation_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = email
    email = EmailMessage(subject, message, to=[to_email])
    email.content_subtype = 'html'
    email.send()
    email_address = request.user.email if request.user.is_authenticated else None
    print("Email sent successfully.")
    return render(request, 'entry/confirmation_sent.html', {'email_address': email_address})


def confirm_email(request, token):
    print("confirming...")
    confirmation = get_object_or_404(EmailConfirmation, token=token)

    # Check if the confirmation link is still valid (e.g., within 24 hours)
    if timezone.now() - confirmation.created_at > timezone.timedelta(hours=24):
        # Token has expired, handle accordingly (e.g., show an error message)
        return render(request, 'entry/confirmation_expired.html')

    # Activate the user's account
    user = confirmation.user
    user.is_active = True
    user.save()

    # Send email confirmation
    send_confirmation_email(user.email, user, request)

    # Delete the confirmation record
    confirmation.delete()

    return redirect('registration_success')



def reset_email_sent(request):
    if request.user.is_authenticated:
        email_address = request.user.email
        print(f"email: {email_address}")
        current_site = get_current_site(request)
        subject = 'Reset Your Password'
        message = render_to_string('entry/reset_email.html', {
            'user': request.user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
            'token': default_token_generator.make_token(request.user),
        })
        to_email = email_address
        email = EmailMessage(subject, message, to=[to_email])
        email.content_subtype = 'html'
        email.send()
    else:
        # If not authenticated, check if the email_address is passed as a parameter
        email_address = request.GET.get('email_address', None)
        print(f"not authenticated email: {email_address}")

    return render(request, 'entry/reset_email_sent.html', {'email_address': email_address})


def password_reset_request(request):

    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = get_user_model().objects.filter(email=email).first()
            if user:
                # Check if the email was sent successfully

                send_email_success = reset_email_sent(request)
                print("The email has been sent successfully")
                if send_email_success:
                    messages.success(request, "Password reset email sent.")
                    return redirect('reset_email_sent')  # Redirect to the reset_email_sent view
                else:
                    messages.error(request, "Failed to send password reset email.")
            else:
                messages.error(request, "User with this email does not exist.")
    else:
        form = PasswordResetForm()

    return render(request, "entry/password_reset.html", {"form": form})



def registration_success(request):
    return render(request, 'entry/registration_success.html')


def confirmation_sent(request):
    return render(request, 'entry/confirmation_sent.html')


def user_login(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Attempting login with username: {username}")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with your desired home view
            else:
                error_message = "Invalid username or password. Please try again."
                return render(request, 'entry/login_prompt.html', {'error_message': error_message})
        else:
            print(f"Form errors: {form.errors}")
            form = UserLoginForm()
    return render(request, 'entry/login_prompt.html', {'form': form})


def view_entry_view(request, entry_id):
    entry = get_object_or_404(DiaryEntry, id=entry_id)

    if request.method == 'POST':
        form = DiaryEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DiaryEntryForm(instance=entry)

    form_data_has_changed = form.has_changed()
    return render(request, 'entry/add_entry.html',
                  {'form': form, 'entry_id': entry_id, 'form_data_has_changed': form_data_has_changed})


def delete_selected_entries_view(request):
    if request.method == 'POST':
        selected_entries = request.POST.getlist('selected_entries')
        DiaryEntry.objects.filter(id__in=selected_entries).delete()

    return redirect('home')


@login_required
def restricted_view(request):
    return render(request, 'restricted.html')


# Option to download entry
def generate_xml(entries):
    # Implement logic to generate XML from diary entries
    # Modify this based on your actual DiaryEntry model structure
    xml_content = f'<diary_entries>{"".join([entry.to_xml() for entry in entries])}</diary_entries>'
    return xml_content


def apply_xslt_transformation(xml_content):
    # Apply XSLT transformation
    xslt_content = loader.get_template('partials/diary_entries.xslt').render()
    xslt_root = etree.fromstring(xslt_content)
    transform = etree.XSLT(xslt_root)
    xml_root = etree.fromstring(xml_content)
    styled_content = transform(xml_root)
    return styled_content


@csrf_exempt
def export_diary_entries(request):
    # Retrieve diary entries (modify as needed based on your model)
    entries = DiaryEntry.objects.all()

    # Generate XML representation of diary entries
    xml_content = generate_xml(entries)

    # Apply XSLT transformation
    styled_content = apply_xslt_transformation(xml_content)

    # Return the styled content as HTML (or other format)
    return HttpResponse(str(styled_content), content_type='text/html')
