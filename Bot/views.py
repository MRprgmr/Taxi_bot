from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View


class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'index.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.add_message(request, messages.WARNING, "Password incorrect")
                return redirect('index')
        else:
            messages.add_message(request, messages.WARNING, "Username incorrect")
            return redirect('index')
