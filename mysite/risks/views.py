from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from .models import Account
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver
import logging
# Create your views here.

# security_logger = logging.getLogger('security')
# @receiver(user_login_failed)
# def on_login_failed(credentials, **kwargs):
#     security_logger.warning(f"Failed login attempt for username: {credentials.get('username')}")

def registerView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Account.objects.create(user=user, balance=0)
            return redirect('/login/')
    else:
        form = UserCreationForm()
    return render(request, 'pages/register.html', {'form': form})

@login_required
# @csrf_exempt
def transferView(request):
    if request.method == 'POST':
        to = User.objects.get(username=request.POST.get('to'))
        amount = int(request.POST.get('amount'))
        if (request.user == to): return redirect('/')
        if not to: return redirect('/')
        if not amount: return redirect('/')
        if amount <= 0: return redirect('/')
        if request.user.account.balance - amount < 0: return redirect('/')

        with transaction.atomic():
            request.user.account.balance -= amount
            to.account.balance += amount
            request.user.account.save()
            to.account.save()
            # A09
            # security_logger.warning(f"Transfer: {request.user.username} sent {amount} to {to.username}")
	
    return redirect('/')

@login_required
def accountView(request, id):
    account = Account.objects.get(id=id)
    # if account.user != request.user:
        # return render(request, "pages/403.html")
    return render(request, 'pages/account.html', {'account': account})

@login_required
def index(request):
	accounts = Account.objects.exclude(user_id=request.user.id)
	return render(request, 'pages/index.html', {'accounts': accounts})