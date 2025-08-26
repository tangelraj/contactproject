from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .forms import ContactForm         # ModelForm (for the second flow)
from .models import ContactSubmission  # used by ModelForm flow


def contact_manual(request):
    """
    Manual HTML form + manual validation.
    Required fields: name, email, message.
    If any field is empty -> show custom error messages.
    We do not save in DB here (this is the manual version).
    """
    errors = {}
    data = {'name': '', 'email': '', 'message': ''}

    if request.method == 'POST':
        data['name'] = request.POST.get('name', '').strip()
        data['email'] = request.POST.get('email', '').strip()
        data['message'] = request.POST.get('message', '').strip()

        if not data['name']:
            errors['name'] = "Please enter your name."
        if not data['email']:
            errors['email'] = "Please enter your email address."
        else:
            # basic server-side email format check
            try:
                validate_email(data['email'])
            except ValidationError:
                errors['email'] = "Please enter a valid email address."
        if not data['message']:
            errors['message'] = "Please write a message."

        if not errors:
            # Success — render success template (not saving to DB)
            return render(request, 'contact/success.html', {'name': data['name'], 'saved': False})

    return render(request, 'contact/contact_manual.html', {'errors': errors, 'data': data})


def contact_model(request):
    """
    ModelForm version. Uses ContactForm and saves to DB on success.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            submission = form.save()
            return render(request, 'contact/success.html', {'name': submission.name, 'saved': True})
    else:
        form = ContactForm()
    return render(request, 'contact/contact_model.html', {'form': form})


def success(request):
    # (not required since views render the success template directly)
    return render(request, 'contact/success.html')
