"""API request handling. Map requests to the corresponding HTMLs."""
import json
import os
from django.http.response import JsonResponse
from django.utils import timezone
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .forms import RegisterForm, LoginForm, ChangePasswordForm, PasswordResetForm
from .models import APIKey, Member

PROTOCOL = "https"

if bool(int(os.environ.get('DEBUG', 1))):
    PROTOCOL = "http"

@login_required(login_url='/login')
def account(request):
    """Render account page"""
    return render(request, "account.html")


def register(request):
    """Render the register page and register a user"""

    form = RegisterForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            current_site = get_current_site(request)

            message = render_to_string('emails/register_email_verification.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': PROTOCOL
            })
            to_email = user.email
            send_mail( subject="Welcome to DelfiTLM",
                message=message,
                from_email = None,
                recipient_list = [to_email],
                fail_silently=True,
                )
            messages.info(request, "Please confirm your email address to complete the registration")
            return redirect("homepage")

        messages.error(request, "Unsuccessful registration")

    return render(request, "registration/register.html", {'form': form})

def activate(request, uidb64, token):
    """Activate user email"""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Member.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.verified = True
        user.save()
        login(request, user)
        Member.objects.filter(username=user.username).update(
                    date_joined=timezone.now(),
                    last_login=timezone.now()
                )
        messages.info(request, "Thank you for your email confirmation. \
                            Now you can login into your account.")
    else:
        messages.error(request, 'Activation link is invalid!')
    return render(request, "home/index.html")


def login_member(request):
    """Render login page"""

    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            entered_username = form.cleaned_data.get('username')
            entered_password = form.cleaned_data.get('password')

            member = authenticate(
                request,
                username=entered_username,
                password=entered_password
            )

            if member is not None and member.verified is False:
                messages.error(request, "Email not verified")
                return render(request, "registration/login.html", {'form': form})

            if member is not None and member.is_active is True:
                login(request, member)
                Member.objects.filter(username=member.username).update(
                        last_login=timezone.now()
                    )
                return render(request, "account.html")

        messages.error(request, "Invalid username or password")

    return render(request, "registration/login.html", { 'form': form })


@login_required(login_url='/login')
def generate_key(request):
    """Generates an API key"""

    if len(APIKey.objects.filter(name=request.user.username))!=0:
        key = APIKey.objects.filter(name=request.user.username)
        key.delete()


    api_key_name, generated_key = APIKey.objects.create_key(
                            name=request.user.username,
                            username=Member.objects.get(username=request.user.username),
    )

    return JsonResponse({"api_key": str(api_key_name), "generated_key": str(generated_key)})


@login_required(login_url='/login')
def get_new_key(request):
    """Render account page with API key"""

    key = json.loads(generate_key(request).content)['generated_key']
    context = {'key': key}
    return render(request, "account.html", context)


@login_required(login_url='/login')
def logout_member(request):
    """Logout and reddirect to homepage"""
    logout(request)

    return redirect('homepage')


@login_required(login_url='/login')
def change_password(request):
    """Render change password page and reset password"""

    form = ChangePasswordForm(request.user)

    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            Member.objects.filter(username=user.username).update(
                        last_changed=timezone.now()
                    )
            messages.info(request, "Password has been changed successfully")
            return redirect('account')

        messages.error(request, "Invalid password")

    return render(request, "registration/change_password.html", {'form': form })


def password_reset_request(request):
    """Send password recovery email"""

    form = PasswordResetForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            entered_email = form.cleaned_data['email']
            if Member.objects.filter(email=entered_email).exists():
                user = Member.objects.get(email=entered_email)
                current_site = get_current_site(request)
                message = render_to_string('emails/password_reset_email.html', {
                    'user': user.username,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': PROTOCOL
                })
                send_mail( subject="DelfiTLM Password Reset Requested",
                    message=message,
                    from_email = None,
                    recipient_list = [entered_email],
                    fail_silently=True,
                    )
                message = "A message with reset password instructions has been sent to your inbox"
                messages.info(request, message)
                return redirect("homepage")

        messages.error(request, "Invalid email address")

    return render(request, "registration/password_reset_form.html", {'form': form})
