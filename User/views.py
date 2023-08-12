from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    FormView,
    ListView,
    DeleteView,
    UpdateView,
    CreateView,
    TemplateView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.utils import timezone

from .forms import SignupForm, LogForm
from .models import AbeUser, Log
from datetime import date

# Create your views here.

class IndexView(LoginRequiredMixin, FormView):
    template_name = "User/index.html"
    form_class = LogForm
    success_url = reverse_lazy("User:index")

    def form_valid(self, form):
        state = form.cleaned_data['state']
        location = form.cleaned_data['location']

        Log.objects.update_or_create(user=self.request.user, date=timezone.now().date(), defaults={'state':state, 'location':location})
        print(timezone.now())
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        today = date.today()
        ctx['today'] = f"{today.year}/{today.month}/{today.day}"

        return ctx
    
class DateView(LoginRequiredMixin, FormView):
    template_name = "User/date.html"
    
class AbeSignUpView(CreateView):
    template_name = 'User/signup.html'
    model = AbeUser
    form_class = SignupForm
    success_url = reverse_lazy('User:index')
    
    def form_valid(self, form):
        result = super().form_valid(form)
        user = self.object
        login(self.request, user)
        return result

class AbeLoginView(LoginView):
    template_name = "User/login.html"
    success_url = reverse_lazy("User:index")

class AbeLogoutView(LoginRequiredMixin, LogoutView):
    pass