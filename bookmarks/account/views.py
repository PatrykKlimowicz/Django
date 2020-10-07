from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm
# Create your views here.


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated correctly!")
                else:
                    return HttpResponse("Failed to authenticate!")
            else:
                return HttpResponse("Invalid login!")
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'account/login.html', context=context)


def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            context = {'new_user': new_user}
            return render(request, 'account/register_done.html', context=context)
    else:
        user_form = UserRegistrationForm()
        context = {'user_form': user_form}
        return render(request, 'account/register.html', context=context)


@login_required
def dashboard(request):
    context = {'section': dashboard}
    return render(request, 'account/dashboard.html', context=context)
