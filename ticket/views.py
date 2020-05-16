from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.http import Http404
from django.views import View
from .forms import *
from .models import *
from django.db.models import Q
from datetime import datetime
from sys_mgr.utils import get_user
from django.utils import timezone


# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class TicketCreateView(CreateView):
    form_class = TicketForm
    template_name = 'ticket/ticket_form.html'
    success_url = '/ticket/list'

    def form_valid(self, form):
        form.instance.create_user = get_user(self.request)
        if form.instance.audit_user:
            form.instance.status = 10
        else:
            form.instance.status = 20
        datetime_string = timezone.now().strftime('%Y%m%d%H%M%S%f')
        if form.instance.type.name == '数据库':
            form.instance.number = 'SD'+datetime_string
        elif form.instance.type.name == '业务服务':
            form.instance.number = 'SY' + datetime_string
        elif form.instance.type.name == '中间件':
            form.instance.number = 'SM' + datetime_string
        else:
            form.instance.number = 'SO' + datetime_string
        return super(TicketCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponse("form is invalid.. this is just an HttpResponse object")


class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('ticket:to_me_list')

    def get_object(self, queryset=None):
        obj = super(TicketDeleteView, self).get_object()
        if not obj.create_user == get_user(self.request):
            raise Http404
        return obj


class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketUpdateForm
    template_name = 'ticket/ticket_form.html'
    success_url = reverse_lazy('ticket:to_me_list')

    def form_valid(self, form):
        form.instance.create_user = get_user(self.request)
        if form.instance.audit_user:
            form.instance.status = 10
        else:
            form.instance.status = 20
        return super(TicketUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print("error:" + str(form.errors))
        return HttpResponse("form is invalid.. this is just an HttpResponse object")


class TicketCancelUpdateView(UpdateView):
    model = Ticket
    form_class = TicketCancelForm
    template_name = 'ticket/ticket_update_form.html'
    success_url = reverse_lazy('ticket:to_me_list')

    def form_valid(self, form):
        if form.instance.create_user == get_user(self.request):
            form.instance.status = -1
        return super(TicketCancelUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print("error:" + str(form.errors))
        return HttpResponse("form is invalid.. this is just an HttpResponse object")

    def get_context_data(self, **kargs):
        context = super().get_context_data(**kargs)
        context['ticket_type'] = 'Cancel'
        return context


class TicketAuditUpdateView(UpdateView):
    model = Ticket
    form_class = TicketAuditForm
    template_name = 'ticket/ticket_update_form.html'
    success_url = reverse_lazy('ticket:to_me_list')

    def form_valid(self, form):
        if form.instance.status == 11:
            form.instance.status = 20
        form.instance.audited_at = timezone.now()
        return super(TicketAuditUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print("error:" + str(form.errors))
        return HttpResponse("form is invalid.. this is just an HttpResponse object")

    def get_context_data(self, **kargs):
        context = super().get_context_data(**kargs)
        context['ticket_type'] = 'Audit'
        return context


class TicketExecuteUpdateView(UpdateView):
    model = Ticket
    form_class = TicketExecuteForm
    template_name = 'ticket/ticket_update_form.html'
    success_url = reverse_lazy('ticket:to_me_list')

    def form_valid(self, form):
        if form.instance.test_user:
            form.instance.status = 30
        else:
            form.instance.status = 40
            form.instance.finished_at = timezone.now()
        form.instance.executed_at = timezone.now()
        return super(TicketExecuteUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print("error:" + str(form.errors))
        return HttpResponse("form is invalid.. this is just an HttpResponse object")

    def get_context_data(self, **kargs):
        context = super().get_context_data(**kargs)
        context['ticket_type'] = 'Execute'
        return context


class TicketTestUpdateView(UpdateView):
    model = Ticket
    form_class = TicketTestForm
    template_name = 'ticket/ticket_update_form.html'
    success_url = reverse_lazy('ticket:to_me_list')

    def form_valid(self, form):
        if form.instance.status == 31:
            form.instance.status = 40
        form.instance.finished_at = timezone.now()
        form.instance.tested_at = timezone.now()
        return super(TicketTestUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        print("error:" + str(form.errors))
        return HttpResponse("form is invalid.. this is just an HttpResponse object")

    def get_context_data(self, **kargs):
        context = super().get_context_data(**kargs)
        context['ticket_type'] = 'Test'
        return context


class TicketListView(ListView):
    model = Ticket
    context_object_name = 'tickets'
    template_name = "ticket/ticket_list.html"


class TicketToMeListView(ListView):
    model = Ticket
    context_object_name = 'tickets'
    template_name = "ticket/ticket_to_me_list.html"

    def get_context_data(self, **kargs):
        context = super().get_context_data(**kargs)
        current_user=get_user(self.request)
        my_all_tickets = Ticket.objects.filter(Q(audit_user=current_user)|Q(execute_user=current_user)|Q(test_user=current_user))
        audit_tickets = Ticket.objects.filter(audit_user=current_user, status=10)
        execute_tickets = Ticket.objects.filter(execute_user=current_user, status=20)
        test_tickets = Ticket.objects.filter(test_user=current_user, status=30)
        all_tickets = [my_all_tickets,audit_tickets,execute_tickets,test_tickets]

        context['all_tickets'] = all_tickets
        context['current_user'] = current_user
        return context


class TicketDetailView(DetailView):
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context