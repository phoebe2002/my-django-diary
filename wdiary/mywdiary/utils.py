from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def send_confirmation_email(to_email, token):
    subject = 'Confirm your email address'
    message = render_to_string('registration_email.html', {'token': token})
    email = EmailMessage(subject, message, to=[to_email])
    email.content_subtype = 'html'  # Set the content type to HTML
    email.send()
