from django.views import View
from django.views.generic import ListView, CreateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse, Http404
from django.shortcuts import reverse, redirect, HttpResponse, get_object_or_404
from django.utils import timezone

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

import time
import json
import _thread
import urllib.request

from .utils import *
from .forms import *
from .models import *
from sys_mgr.utils import get_user
from mysite.settings import GIT_HOST, GIT_PRIVATE_TOKEN


class ProjectTagsView(View):
    def get(self, request):
        """
        获取GIT标签版本
        """
        service_id = request.GET.get('service_id')
        try:
            service = Service.objects.get(id=service_id)
        except Exception as e:
            service = None
        if not service:
            return JsonResponse({'errno': -1, 'errmsg': 'id error', 'data': {}}, safe=False)
        git_host = GIT_HOST
        private_token = GIT_PRIVATE_TOKEN
        project_id = service.project.repository.vcs_project_id
        response = urllib.request.urlopen(
            url="http://{0}/api/v4/projects/{1}/repository/tags?private_token={2}".format(git_host,project_id,
                                                                                          private_token))
        reps = response.read().decode("utf-8")
        tags_json = json.loads(reps)
        tags_list = []
        for tag in tags_json[:30]:
            tags_list.append('refs/tags/'+tag['name'])

        response = urllib.request.urlopen(
            url="http://{0}/api/v4/projects/{1}/repository/branches?private_token={2}".format(git_host, project_id,
                                                                                          private_token))
        reps = response.read().decode("utf-8")
        branches_json = json.loads(reps)
        branches_list = []
        for branch in branches_json[:30]:
            branches_list.append('*/' + branch['name'])
        return JsonResponse({'errno': 0, 'errmsg': 'ok', 'data': tags_list+branches_list}, safe=False)


class GetAllJobsProgress(View):
    def get(self, request):
        jobs_data_list = []
        for job in Job.objects.all():
            #通过状态判断jobplan是否执行，如果没有执行则直接构造列表
            if job.status == 0:
                jobs_data_list.append({'job_id': job.id, 'progress': 100})
            else:
                #获取最新job_plan的创建时间
                last_job_plan = job.job_plans.order_by('-created_at')[0]
                print(timezone.now(), last_job_plan.created_at)
                last_job_plan_duration_seconds = (timezone.now() - last_job_plan.created_at).total_seconds()
                job_plans_queryset = job.job_plans.order_by('-finished_at')[:2]
                if job_plans_queryset.count() == 2:
                    total_seconds = 0
                    for job_plan in job_plans_queryset:
                        total_seconds += job_plan.duration/1000.0
                    average_seconds = total_seconds / 2
                    print(last_job_plan_duration_seconds, average_seconds)
                    estimate_progress = last_job_plan_duration_seconds / average_seconds * 0.5 * 100
                else:
                    estimate_progress = last_job_plan_duration_seconds * 0.5
                progress = 95 if estimate_progress > 95 else estimate_progress
                jobs_data_list.append({'job_id': job.id, 'progress': progress})
            #如果在执行，获取最近2次的该job的构建时间取平均值，否则执行时间，通过执行的秒数*5并且如果结果大于95，设置值为95
        return JsonResponse({'errno': 0, 'errmsg': 'ok', 'data': jobs_data_list}, safe=False)


class JobCreateView(CreateView):
    form_class = JobForm
    template_name = 'deploy/job_form.html'
    success_url = '/deploy/job/list'

    def form_valid(self, form):
        form.instance.create_user = get_user(self.request)
        return super(JobCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponse("form is invalid.. this is just an HttpResponse object")


class JobPlanCreateView(CreateView):
    form_class = JobPlanForm
    template_name = 'deploy/job_plan_form.html'
    success_url = '/deploy/job/list'

    def dispatch(self, request, *args, **kwargs):
        """
         获取job_id得到job对象
        """
        try:
            job = get_object_or_404(Job, pk=kwargs['job_id'])
            self.job = job
            self.name = job.name
        except:
            pass
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        #生成job_plan对象
        super(JobPlanCreateView, self).post(request)
        #调用jenkins接口执行升级
        try:
            jenkins_job = JenkinsJob.objects.get(space=self.object.job.space, service=self.object.job.service)
            if self.object.job.space.name == '生产':
                env = 'prod'
            elif self.object.job.space.name == '预生产':
                env = 'pre_prod'
            elif self.object.job.space.name == '测试':
                env = 'test'
            elif self.object.job.space.name == '研发':
                env = 'dev'
            else:
                env = 'unknow'
            last_build_number = get_last_build_number(env, jenkins_job.job_name)
            #判断构建状态
            build_job_branch_tag(env, jenkins_job.job_name, self.object.vcs_tag)
            # 设置job 的状态为构建中
            self.object.jenkins_build_number = last_build_number + 1
            self.object.job.status = 1
            self.object.job.save()
            _thread.start_new_thread(self.update_job_info, (env, jenkins_job.job_name))
            message = "发布中"
        except Exception as e:
            message = "发布异常"
        return redirect(reverse("deploy:job_list"))

    def update_job_info(self, space, job_name):
        # 设置job默认为失败
        self.object.status = 2
        _start_count = 0
        while _start_count < 600:
            if get_job_build_result(space, job_name, self.object.jenkins_build_number) == 'SUCCESS':
                self.object.status = 1
                break
            elif get_job_build_result(space, job_name, self.object.jenkins_build_number) == 'FAILURE':
                self.object.status = 2
                break
            _start_count += 1
            time.sleep(1)

        if _start_count >= 600:
            self.object.status = 3
        # 更新job_plan的状态
        self.object.finished_at = timezone.now()
        self.object.duration = get_job_build_info(space, job_name, self.object.jenkins_build_number)['duration']
        self.object.console_output = get_job_build_console_output(space, job_name, self.object.jenkins_build_number)
        self.object.save()
        # 更新job的状态
        self.object.job.status = 0
        self.object.job.save()

    def get_initial(self, *args, **kwargs):
        initial = super(JobPlanCreateView, self).get_initial(**kwargs)
        datetime_string = timezone.now().strftime('%Y%m%d%H%M%S')
        initial['name'] = "{0}-{1}".format(self.job.name, datetime_string)
        initial['job'] = self.job
        initial['job_type'] = 1
        initial['created_type'] = 1
        initial['project'] = self.job.service.project
        initial['service'] = self.job.service
        return initial

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        form = super(JobPlanCreateView, self).get_form(form_class)
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.job
        return context

    def form_valid(self, form):
        form.instance.execute_user = get_user(self.request)
        form.instance.status = 0
        form.instance.created_at = timezone.now()
        return super(JobPlanCreateView, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponse("form is invalid.. this is just an HttpResponse object")


class JobListView(ListView):
    model = Job
    context_object_name = 'jobs'
    template_name = "deploy/job_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = get_user(self.request)
        return context


class JobPlanListView(ListView):
    model = JobPlan
    context_object_name = 'job_plans'
    template_name = "deploy/job_plan_list.html"

    def get_queryset(self):
        try:
            job = get_object_or_404(Job, pk=self.kwargs['job_id'])
            self.job = job
            queryset = JobPlan.objects.filter(job=job)
        except:
            queryset = JobPlan.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.job
        return context


class JobDetailView(DetailView):
    model = Job


class JobPlanDetailView(DetailView):
    model = JobPlan
    template_name = 'deploy/job_plan_detail.html'


class JobUpdateView(UpdateView):
    model = Job
    form_class = JobUpdateForm
    template_name = 'deploy/job_form.html'
    success_url = reverse_lazy('deploy:job_list')

    def form_invalid(self, form):
        print("error:" + str(form.errors))
        return HttpResponse("form is invalid.. this is just an HttpResponse object")


class JobDeleteView(DeleteView):
    model = Job
    success_url = reverse_lazy('deploy:job_list')

    def get_object(self, queryset=None):
        obj = super(JobDeleteView, self).get_object()
        if not obj.create_user == get_user(self.request):
            raise Http404
        return obj


class JobPlanUpdateView(UpdateView):
    model = Job
    form_class = JobPlanUpdateForm
    template_name = 'deploy/ticket_form.html'
    success_url = reverse_lazy('deploy:job_list')

    def form_invalid(self, form):
        print("error:" + str(form.errors))
        return HttpResponse("form is invalid.. this is just an HttpResponse object")



#开启定时工作
try:
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # 设置定时任务，选择方式为interval，时间间隔为10s
    # 另一种方式为每天固定时间执行任务，对应代码为：
    # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
    @register_job(scheduler,"interval", seconds=10)
    def update_job_plan_status_job():
        print("定时器OK")
        # 获取所有job_plan为进行中的状态
        for job_plan in JobPlan.objects.filter(status=0):
            jenkins_job = JenkinsJob.objects.get(space=job_plan.job.space, service=job_plan.job.service)
            job_build_info=get_job_build_info(job_plan.job.space, jenkins_job.job_name, job_plan.jenkins_build_number)
            result = job_build_info['result']
            if result:
                #更新job_plan
                if result == 'SUCCESS':
                    job_plan.status = 1
                elif result == 'FAILURE':
                    job_plan.status = 2
                fin
                #更新job

    register_events(scheduler)
    scheduler.start()
except Exception as e:
    print(e)
    # 有错误就停止定时器
    scheduler.shutdown()
