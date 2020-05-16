from django.urls import path
from .views import *


app_name = "deploy"
urlpatterns = [
    path('project/tags', ProjectTagsView.as_view(), name='tags'),
    path('job/build', JobCreateView.as_view(), name='job_build'),
    path('job/add', JobCreateView.as_view(), name='job_add'),
    path('job/list', JobListView.as_view(), name='job_list'),
    path('job_plan/add/job/<int:job_id>', JobPlanCreateView.as_view(), name='job_plan_add'),
    path('job/update/<int:pk>', JobUpdateView.as_view(), name='job_update'),
    path('job/detail/<int:pk>', JobDetailView.as_view(), name='job_detail'),
    path('job/delete/<int:pk>', JobDeleteView.as_view(), name='job_delete'),
    path('job_plan/list/<int:job_id>', JobPlanListView.as_view(), name='job_plan_list'),
    path('job_plan/detail/<int:pk>', JobPlanDetailView.as_view(), name='job_plan_detail'),
    path('job_plan/update/<int:pk>', JobPlanUpdateView.as_view(), name='job_plan_update'),
    path('job/progress', GetAllJobsProgress.as_view(), name='get_all_jobs_process'),
]