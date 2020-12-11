from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate

from payments.decorators.decorators import unauthenticated_user
from payments.forms.forms import CreateCompanyForm
from payments.models import Payment


@unauthenticated_user
def registerPage(request):
    form = CreateCompanyForm()
    if request.method == 'POST':
        form = CreateCompanyForm(request.POST)
        if form.is_valid():
            try:
                company = form.save()
                company_name = form.cleaned_data.get('name')

                messages.success(request, 'Account was created for ' + company_name)

                return redirect('login')
            except Exception as error:
                msg = error.message
                messages.error(request, msg)

    context = {'form': form}
    return render(request, 'login/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    payment_list = request.user.payment_set.all()

    context = {
        'payment_list': payment_list,
        'total_payments': payment_list.count(),
        'successful': payment_list.filter(status=Payment.STATUS_SUCCESSFUL).count(),
        'failed': payment_list.filter(status=Payment.STATUS_FAILED).count(),
        'disputed': payment_list.filter(status=Payment.STATUS_DISPUTED).count(),
        'created': payment_list.filter(status=Payment.STATUS_CREATED).count(),
    }
    return render(request, 'customer/dashboard_user.html', context)


