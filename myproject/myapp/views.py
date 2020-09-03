from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user, allowed_users, admin_only

from .models import *
from .forms import IssueForm, CreateUserForm, CustomerForm
from .filters import IssueFilter


# Create your views here.

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, "Account successfully created for " + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'myapp/register.html', context)


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
            messages.info(request, "Invalid Credentials")

    return render(request, 'myapp/login.html')


def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    issues = request.user.customer.issue_set.all()
    t_issues = issues.count()
    pending = issues.filter(status="Pending").count()
    in_progress = issues.filter(status="In Progress").count()
    just_receive = issues.filter(status="Just Receive").count()
    closed = issues.filter(status="Closed").count()

    context = {
        'issues': issues,
        't_issues': t_issues,
        'pending': pending,
        'in_progress': in_progress,
        'just_receive': just_receive,
        'closed': closed,
    }
    return render(request, 'myapp/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
    }
    return render(request, 'myapp/account_settings.html', context)


@login_required(login_url='login')
@admin_only
def home(request):
    issues = Issue.objects.all()
    customers = Customer.objects.all()
    t_issues = issues.count()
    t_customers = customers.count()
    pending = issues.filter(status="Pending").count()
    in_progress = issues.filter(status="In Progress").count()
    just_receive = issues.filter(status="Just Receive").count()
    closed = issues.filter(status="Closed").count()

    context = {
        'issues': issues,
        'customers': customers,
        't_issues': t_issues,
        't_customers': t_customers,
        'pending': pending,
        'in_progress': in_progress,
        'just_receive': just_receive,
        'closed': closed,
    }
    return render(request, 'myapp/index.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    p = Product.objects.all()
    return render(request, 'myapp/product.html', {'p': p})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk):
    c = Customer.objects.get(id=pk)
    issues = c.issue_set.all()
    t_issues = issues.count()
    myFilter = IssueFilter(request.GET, queryset=issues)
    issues = myFilter.qs

    context = {
        'c': c,
        'issues': issues,
        't_issues': t_issues,
        'myFilter': myFilter,
    }
    return render(request, 'myapp/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createIssue(request, pk):
    IssueFormSet = inlineformset_factory(Customer, Issue, fields= ('product', 'status'))
    customers = Customer.objects.get(id=pk)
    formset = IssueFormSet(queryset = Issue.objects.none(), instance=customers)
    if request.method == 'POST':
        formset = IssueFormSet(request.POST, instance=customers)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        'formset': formset,
    }
    return render(request, 'myapp/issue_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateIssue(request, pk):
    issues = Issue.objects.get(id=pk)
    form = IssueForm(instance=issues)
    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issues)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form,
    }
    return render(request, 'myapp/issue_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteIssue(request, pk):
    item = Issue.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('/')

    context = {
        'item': item,
    }
    return render(request, 'myapp/delete.html', context)












