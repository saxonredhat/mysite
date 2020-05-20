from django.views.generic import ListView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
from django.views import View
from django.shortcuts import reverse, render, redirect, HttpResponse, get_object_or_404

from .forms import *
from .models import *
from django.db.models import Q
from datetime import datetime
from sys_mgr.utils import get_user
from django.utils import timezone

from deploy.models import Job, JobPlan, JenkinsJob
from deploy.utils import *
import json


# Create your views here.
class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


def ticket_bind_info(request):
    type_id = request.GET.get('type_id')
    space_id = request.GET.get('space_id')
    service_id = request.GET.get('service_id')
    ticket_bind_info = TicketBindInfo.objects.filter(type__id=type_id, space__id=space_id, service__id=service_id).first()
    print("ticket_bind_info:{0}".format(ticket_bind_info))
    #判断工单是否有做人员绑定
    if not ticket_bind_info:
        audit_users_list = []
        execute_users_list = []
        test_users_list = []
        try:
            space = Space.objects.get(id=space_id)
        except:
            space = None
        if space and space.code == 'TEST':
            robot = User.objects.get(username='robot')
            execute_users_list.append({'execute_user_id': robot.id,
                                       'execute_user_name': robot.chinese_name})
            is_bind = 1
        else:
            audit_users = User.objects.filter(position__name="审核人员")
            execute_users = User.objects.filter(position__name="运维人员")
            test_users = User.objects.filter(position__name="测试人员")

            for audit_user in audit_users:
                audit_users_list.append({'audit_user_id': audit_user.id, 'audit_user_name': audit_user.chinese_name})
            for execute_user in execute_users:
                execute_users_list.append({'execute_user_id': execute_user.id,
                                           'execute_user_name': execute_user.chinese_name})
            for test_user in test_users:
                test_users_list.append({'test_user_id': test_user.id, 'test_user_name': test_user.chinese_name})
            is_bind = 0

        data = {'bind': is_bind, 'audit_users_list': audit_users_list, 'execute_users_list': execute_users_list,
                'test_users_list': test_users_list}
    else:
        audit_users_list = []
        execute_users_list = []
        test_users_list = []

        if ticket_bind_info.audit_user:
            audit_users_list.append({'audit_user_id': ticket_bind_info.audit_user.id,
                                     'audit_user_name': ticket_bind_info.audit_user.chinese_name})

        if ticket_bind_info.execute_user:
            execute_users_list.append({'execute_user_id': ticket_bind_info.execute_user.id,
                                     'execute_user_name': ticket_bind_info.execute_user.chinese_name})

        if ticket_bind_info.test_user:
            test_users_list.append({'test_user_id': ticket_bind_info.test_user.id,
                                     'test_user_name': ticket_bind_info.test_user.chinese_name})
        data = {'bind': 1, 'audit_users_list': audit_users_list, 'execute_users_list': execute_users_list,
                    'test_users_list': test_users_list}
    return JsonResponse({'errno': 0, 'errmsg': 'ok', 'data': data}, safe=False)


def create_job_plan(ticket):
    space = ticket.space
    service = ticket.service
    job = Job.objects.get(space=space, service=service)
    jenkins_job = JenkinsJob.objects.get(space=space, service=service)
    datetime_string = timezone.now().strftime('%Y%m%d%H%M%S')
    job_plan_name = "{0}-{1}".format(job.name, datetime_string)
    job_name = jenkins_job.job_name
    next_build_number = get_next_build_number(space, job_name)
    job_plan = JobPlan(name=job_plan_name, job=job, ticket=ticket, vcs_tag=ticket.vcs_tag,
                       execute_user=ticket.execute_user, job_type=2, created_type=2,
                       jenkins_build_number=next_build_number)
    build_job_branch_tag(space, job_name, ticket.vcs_tag)
    # 设置job 的状态为构建中
    job_plan.save()
    job_plan.job.status = 1
    job_plan.job.save()


def create_job_plan_by_robot(ticket):
    if ticket.execute_user.username == 'robot':
        create_job_plan(ticket)


def create_job_plan_by_user(ticket):
    create_job_plan(ticket)


class TicketCreateView(CreateView):
    form_class = TicketForm
    template_name = 'ticket/ticket_form.html'
    success_url = '/ticket/list'

    def post(self, request, *args, **kwargs):
        super(TicketCreateView, self).post(request)
        try:
            if not self.object.is_need_audit():
                create_job_plan_by_robot(self.object)
        except Exception as e:
            print(e)
        return redirect(reverse("ticket:list"))

    def get_initial(self, *args, **kwargs):
        initial = super(TicketCreateView, self).get_initial(**kwargs)
        try:
            ticket_type = TicketType.objects.get(code="BUSINESS_SERVICE")
            space = Space.objects.get(code="TEST")
            initial['type'] = ticket_type
            initial['space'] = space
        except:
            pass
        return initial

    def form_valid(self, form):
        form.instance.create_user = get_user(self.request)
        form.instance.create_update_info()
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


class TicketCreateFromTicketView(CreateView):
    form_class = TicketFromTicketForm
    template_name = 'ticket/ticket_add_from_ticket_form.html'
    success_url = '/ticket/list'

    def post(self, request, *args, **kwargs):
        super(TicketCreateFromTicketView, self).post(request)
        try:
            if not self.object.is_need_audit():
                create_job_plan_by_robot(self.object)
        except Exception as e:
            print(e)
        return redirect(reverse("ticket:list"))

    def get_initial(self, *args, **kwargs):
        initial = super(TicketCreateFromTicketView, self).get_initial(**kwargs)
        print("get_initial")
        try:
            ticket_id = self.kwargs['ticket_id']
            space_code = self.kwargs['space_code']
            try:
                ticket = Ticket.objects.get(pk=ticket_id)
            except:
                ticket = None

            try:
                space = Space.objects.get(code=space_code)
            except:
                space = Space.objects.get(code="TEST")
            if ticket and space.code != 'TEST':
                ticket_type = ticket.type
                parent = ticket
                title = "[{0}]{1}".format(space.name, ticket.title)
                service = ticket.service
                vcs_tag = ticket.vcs_tag
                service_conf = ticket.service_conf
                db_conf = ticket.db_conf
                db_file = ticket.db_file
                other_conf = ticket.db_conf
                initial['type'] = ticket_type
                initial['parent'] = parent
                initial['title'] = title
                initial['space'] = space
                initial['service'] = service
                initial['vcs_tag'] = vcs_tag
                initial['service_conf'] = service_conf
                initial['db_conf'] = db_conf
                initial['db_file'] = db_file
                initial['other_conf'] = other_conf
        except Exception as e:
            print(e)
        return initial

    def form_valid(self, form):
        form.instance.create_user = get_user(self.request)
        form.instance.create_update_info()
        datetime_string = timezone.now().strftime('%Y%m%d%H%M%S%f')
        if form.instance.type.name == '数据库':
            form.instance.number = 'SD' + datetime_string
        elif form.instance.type.name == '业务服务':
            form.instance.number = 'SY' + datetime_string
        elif form.instance.type.name == '中间件':
            form.instance.number = 'SM' + datetime_string
        else:
            form.instance.number = 'SO' + datetime_string
        return super(TicketCreateFromTicketView, self).form_valid(form)

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
        form.instance.create_update_info()
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

    def post(self, request, *args, **kwargs):
        super(TicketAuditUpdateView, self).post(request)
        try:
            if self.object.audit_approved():
                self.object.audit_update_info()
                create_job_plan_by_robot(self.object)
            else:
                self.object.audit_update_info()
        except Exception as e:
            print(e)
        return redirect(reverse("ticket:to_me_list"))

    def form_valid(self, form):
        #if form.instance.status == 11:
        #    form.instance.status = 20
        #form.instance.audited_at = timezone.now()
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

    def post(self, request, *args, **kwargs):
        super(TicketExecuteUpdateView, self).post(request)
        try:
            create_job_plan_by_user(self.object)
        except Exception as e:
            print(e)
        return redirect(reverse("ticket:to_me_list"))

    def form_valid(self, form):
        #form.instance.execute_update_info()
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
        my_all_tickets = Ticket.objects.filter(Q(create_user=current_user)|Q(audit_user=current_user)|Q(execute_user=current_user)|Q(test_user=current_user))
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