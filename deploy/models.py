from django.db import models
from .constant import *


class Project(models.Model):
	name = models.CharField(max_length=64, verbose_name='项目名')
	description = models.CharField(max_length=256, verbose_name='项目说明', blank=True, null=True)
	repository = models.OneToOneField("Repository", verbose_name="版本仓库", on_delete=models.CASCADE,
	                                  related_name='project', blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = u"项目"
		verbose_name_plural = verbose_name


class Service(models.Model):
	name = models.CharField(max_length=64, verbose_name='服务名')
	description = models.CharField(max_length=256, verbose_name='服务说明', blank=True, null=True)
	project = models.ForeignKey("Project", verbose_name="项目", on_delete=models.CASCADE, related_name='services')

	def __str__(self):
		return "{0}({1})".format(self.name, self.project.name)

	class Meta:
		verbose_name = u"服务"
		verbose_name_plural = verbose_name


class Repository(models.Model):
	name = models.CharField(max_length=64, verbose_name='仓库名')
	description = models.CharField(max_length=256, verbose_name='仓库说明', blank=True, null=True)
	vcs_project_id = models.IntegerField(verbose_name='版本项目ID', blank=True, null=True)
	vcs_type = models.SmallIntegerField(choices=REPOSITORY_TYPE, verbose_name='版本库类型')
	vcs_url = models.CharField(max_length=512, verbose_name='版本库地址', blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = u"仓库"
		verbose_name_plural = verbose_name


class JenkinsJob(models.Model):
	service = models.ForeignKey("Service", verbose_name="服务", on_delete=models.CASCADE, related_name='jenkins_jobs')
	space = models.ForeignKey('sys_mgr.Space', verbose_name="空间", on_delete=models.CASCADE, related_name='jenkins_jobs')
	job_name = models.CharField("Jenkins-Job", max_length=256, null=False, blank=False, default="")

	def __str__(self):
		return "[{0}]-[{1}]-[{2}]".format(self.space,self.service,self.job_name)

	class Meta:
		verbose_name = u"Jenkins-Job"
		verbose_name_plural = verbose_name


class Job(models.Model):
	name = models.CharField("发布名", max_length=256, null=False, blank=False, default="")
	description = models.TextField("发布描述", blank=True, null=True)
	service = models.ForeignKey("Service", verbose_name="服务", on_delete=models.CASCADE, related_name='jobs')
	create_user = models.ForeignKey('sys_mgr.User', verbose_name="创建用户", on_delete=models.CASCADE, related_name='jobs',blank=True ,null=True)
	space = models.ForeignKey('sys_mgr.Space', verbose_name="空间", on_delete=models.CASCADE, related_name='jobs')
	status = models.SmallIntegerField("状态", blank=True, default=0)

	def __str__(self):
		return self.name

	def get_status_name(self):
		if self.status == 0:
			return "空闲"
		elif self.status == 1:
			return "构建中"
		return "未知"

	class Meta:
		verbose_name = u"发布"
		verbose_name_plural = verbose_name


class JobPlan(models.Model):
	name = models.CharField("发布计划名", max_length=64, unique=True)
	job = models.ForeignKey("Job", verbose_name="发布", on_delete=models.CASCADE, related_name='job_plans')
	ticket = models.ForeignKey("ticket.Ticket", verbose_name="关联工单", on_delete=models.CASCADE,
	                           related_name='job_plans', blank=True, null=True)
	vcs_tag = models.CharField("分支或标签", max_length=256, blank=True, null=True)
	execute_user = models.ForeignKey("sys_mgr.User", verbose_name="执行人员", on_delete=models.CASCADE,
	                                 related_name='job_plans', blank=True, null=True)
	job_type = models.SmallIntegerField("发布方式", choices=JOB_TYPE, blank=True, default=0)
	created_type = models.SmallIntegerField("创建类型", choices=CREATED_TYPE, blank=True, default=0)
	duration = models.IntegerField("构建时长", default=0, blank=True, null=True)
	jenkins_build_number = models.IntegerField("jenkins构建号", blank=True, null=True)
	#jenkins_job = models.ForeignKey("JenkinsJob", verbose_name="jenkins构建Job对象", blank=True, null=True)
	status = models.SmallIntegerField("结果", blank=True, default=0)
	detail_description = models.TextField("发布计划详情", blank=True, null=True)
	console_output = models.TextField("发布console信息", blank=True, null=True)
	finished_at = models.DateTimeField("完成时间", blank=True, null=True)
	created_at = models.DateTimeField("创建时间", auto_now_add=True)

	def __str__(self):
		return self.name

	def get_job_type_name(self):
		job_type = ''
		for k, v in JOB_TYPE:
			if k == self.job_type:
				job_type = v
		return job_type

	def get_created_type_name(self):
		created_type = ''
		for k, v in CREATED_TYPE:
			if k == self.created_type:
				created_type = v
		return created_type

	def get_status_name(self):
		if self.status == 0:
			return "构建中"
		elif self.status == 1:
			return "成功"
		elif self.status == 2:
			return "失败"
		return "未知"

	class Meta:
		verbose_name = u"发布计划"
		verbose_name_plural = verbose_name
