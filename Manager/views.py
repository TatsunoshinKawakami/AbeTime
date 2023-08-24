from typing import Any, Dict
from django import http
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
from django.utils import timezone
from django import forms

from User.models import Log, AbeUser

import datetime
from dateutil.relativedelta import relativedelta

# Create your views here.

class ManagerIndexView(LoginRequiredMixin, TemplateView):
    template_name = 'Manager/index.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_staff:
            return redirect(reverse_lazy('User:index'))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        users = AbeUser.objects.filter(is_staff=False).order_by('id')
        ctx['users'] = users
        
        date_start : datetime.date
        date_end : datetime.date
        today = datetime.date.today()
        if today.day > 25:
            date_start = datetime.datetime(f"{today.year}-{today.month}-26", '%Y-%m-%d').date()
            date_end = date_start + relativedelta(months=1) - datetime.timedelta(days=1)
        else:
            date_end = datetime.datetime.strptime(f"{today.year}-{today.month}-25", '%Y-%m-%d').date()
            date_start = date_end - relativedelta(months=1) + datetime.timedelta(days=1)
        ctx['date_start'] = date_start
        ctx['date_end'] = date_end
        ctx['pre_date_start'] = date_start - relativedelta(months=1)

        counts = []
        map_time = [1, 0.5, 0]
        for user in users:
            counts.append(sum([map_time[x.state] for x in Log.objects.filter(user=user, date__range=[date_start, date_end])]))
        ctx['counts'] = counts
        
        choices = [(0, '◯'), ('1', '△'), ('2', '✕'), ('3', '---')]
        date_logs = []
        for i in range((date_end - date_start).days + 1):
            logs = []
            for user in users:
                log = Log.objects.filter(user=user, date=date_start).first()
                form = forms.Form()
                if log == None:
                    form.fields['state_' + user.username + '_' + str(date_start)] = forms.ChoiceField(widget=forms.widgets.Select(attrs={'class': 'form-control', 'style': 'font-size: 0.8em'}), label='', choices=choices, initial=3)
                    form.fields['location_' + user.username + '_' + str(date_start)] = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'style': 'font-size: 0.8em'}), label='', required=False)
                    logs.append(form)
                else:
                    form.fields['state_' + user.username + '_' + str(date_start)] = forms.ChoiceField(widget=forms.widgets.Select(attrs={'class': 'form-control', 'style': 'font-size: 0.8em'}), label='', choices=choices, initial=log.state)
                    form.fields['location_' + user.username + '_' + str(date_start)] = forms.CharField(widget=forms.widgets.TextInput(attrs={'class': 'form-control', 'style': 'font-size: 0.8em'}), label='', required=False, initial=log.location)
                    logs.append(form)
            date_logs.append((date_start, logs))
            date_start = date_start + datetime.timedelta(days=1)
        ctx['date_logs'] = date_logs

        return ctx
    
    def post(self, request, *args, **kwargs):
        date_start : datetime.date
        date_end : datetime.date
        today = datetime.date.today()
        if today.day > 25:
            date_start = datetime.datetime(f"{today.year}-{today.month}-26", '%Y-%m-%d').date()
            date_end = date_start + relativedelta(months=1) - datetime.timedelta(days=1)
        else:
            date_end = datetime.datetime.strptime(f"{today.year}-{today.month}-25", '%Y-%m-%d').date()
            date_start = date_end - relativedelta(months=1) + datetime.timedelta(days=1)

        for i in range((date_end - date_start).days + 1):
            for user in AbeUser.objects.filter(is_staff=False).order_by('id'):
                state = int(request.POST.get('state_' + user.username + '_' + str(date_start)))
                location = request.POST.get('location_' + user.username + '_' + str(date_start))
                if state != 3:
                    Log.objects.update_or_create(user=user, date=date_start, defaults={'state':state, 'location':location})
            date_start = date_start + datetime.timedelta(days=1)
            
        return redirect(reverse_lazy('Manager:index'))

    
class ManagerDateView(LoginRequiredMixin, TemplateView):
    template_name = 'Manager/date.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        users = AbeUser.objects.filter(is_staff=False).order_by('id')
        ctx['users'] = users
        
        date_start = datetime.datetime.strptime(str(self.kwargs.get('year'))+'-'+str(self.kwargs.get('month'))+'-'+str(self.kwargs.get('day')), '%Y-%m-%d').date()
        date_end = date_start + relativedelta(months=1) - datetime.timedelta(days=1)
        ctx['date_start'] = date_start
        ctx['date_end'] = date_end
        ctx['pre_date_start'] = date_start - relativedelta(months=1)
        ctx['next_date_start'] = date_start + relativedelta(months=1)
        if date_end < timezone.now().today().date():
            ctx['is_safe_date'] = True
        
        date_logs = []
        for i in range((date_end - date_start).days + 1):
            logs = []
            for user in users:
                log = Log.objects.filter(user=user, date=date_start).first()
                if log == None:
                    logs.append(Log(state=4))
                else:
                    logs.append(log)
            date_logs.append((date_start, logs))
            date_start = date_start + datetime.timedelta(days=1)
        ctx['date_logs'] = date_logs

        return ctx