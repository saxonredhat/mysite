from django.shortcuts import HttpResponse, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views import View
from .forms import TicketForm
from .models import *
from django.db.models import Q
import re

def get_user(request):
    try:
        card = User.objects.get(id=request.session['user_id'])
    except:
        card = None
    return card

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
        return super(TicketCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponse("form is invalid.. this is just an HttpResponse object")


class TicketUpdateView(UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'ticket/ticket_form.html'
    success_url = '/ticket/list'

    def form_invalid(self, form):
        return HttpResponse("form is invalid.. this is just an HttpResponse object")

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
        audit_tickets = Ticket.objects.filter(audit_user=current_user,status__gte=10)
        execute_tickets = Ticket.objects.filter(execute_user=current_user,status__gte=20)
        test_tickets = Ticket.objects.filter(test_user=current_user,status__gte=30)
        all_tickets = [audit_tickets,execute_tickets,test_tickets]

        context['all_tickets'] = all_tickets
        return context


class TicketDetailView(DetailView):
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context