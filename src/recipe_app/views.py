from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    error_message = None
    form = AuthenticationForm()

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("recipes:list")
        else:
            error_message = "Username and/or Password were incorrect. Please try again."

    context = {"form": form, "error_message": error_message}

    return render(request, "auth/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("recipes:list")  # Redirect to recipe list instead of success page


def success_view(request):
    return render(request, "auth/success.html")
