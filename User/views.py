from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    FormView,
    ListView,
    DeleteView,
    UpdateView,
    CreateView,
    TemplateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.utils import timezone

from .forms import LoginForm, LogForm, DateSelectForm
from .models import AbeUser, Log
from datetime import date, datetime, timedelta

# Create your views here.


class IndexView(LoginRequiredMixin, FormView):
    template_name = "User/index.html"
    form_class = LogForm
    success_url = reverse_lazy("User:index")

    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            return redirect(reverse_lazy("Manager:index"))

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        state = form.cleaned_data["state"]
        well_known_location = form.cleaned_data["well_known_location"]
        location = form.cleaned_data["location"]

        Log.objects.update_or_create(
            user=self.request.user,
            date=timezone.now().date(),
            defaults={"state": state, "well_known_location": well_known_location, "location": location},
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        today = date.today()
        ctx["today"] = f"{today.year}/{today.month}/{today.day}"
        ctx["previous_date"] = today - timedelta(days=1)

        ctx["log"] = Log.objects.filter(
            user=self.request.user, date=timezone.now().date()
        ).first()

        return ctx


class DateView(LoginRequiredMixin, FormView):
    template_name = "User/date.html"
    form_class = LogForm

    def form_valid(self, form):
        self.success_url = reverse_lazy(
            "User:date",
            kwargs={
                "year": self.kwargs.get("year"),
                "month": self.kwargs.get("month"),
                "day": self.kwargs.get("day"),
            },
        )

        state = form.cleaned_data["state"]
        well_known_location = form.cleaned_data["well_known_location"]
        location = form.cleaned_data["location"]
        this_date = datetime.strptime(
            str(self.kwargs.get("year"))
            + "-"
            + str(self.kwargs.get("month"))
            + "-"
            + str(self.kwargs.get("day")),
            "%Y-%m-%d",
        ).date()

        Log.objects.update_or_create(
            user=self.request.user,
            date=this_date,
            defaults={"state": state, "well_known_location": well_known_location, "location": location},
        )

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        this_date = datetime.strptime(
            str(self.kwargs.get("year"))
            + "-"
            + str(self.kwargs.get("month"))
            + "-"
            + str(self.kwargs.get("day")),
            "%Y-%m-%d",
        )
        ctx["is_safe_date"] = this_date.date() < date.today()
        ctx["this_date"] = f"{this_date.year}/{this_date.month}/{this_date.day}"
        ctx["next_date"] = this_date + timedelta(days=1)
        ctx["previous_date"] = this_date - timedelta(days=1)

        ctx["log"] = Log.objects.filter(user=self.request.user, date=this_date).first()

        return ctx


class DateSelectView(FormView):
    template_name = "User/date_select.html"
    form_class = DateSelectForm

    def form_valid(self, form):
        year = form.cleaned_data["year"]
        month = form.cleaned_data["month"]
        day = form.cleaned_data["day"]

        self.success_url = reverse_lazy(
            "User:date", kwargs={"year": year, "month": month, "day": day}
        )

        return super().form_valid(form)


class AbeLoginView(LoginView):
    template_name = "User/login.html"
    success_url = reverse_lazy("User:index")
    form_class = LoginForm


class AbeLogoutView(LoginRequiredMixin, LogoutView):
    pass
