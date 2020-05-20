from django.db import models
from deploy.models import Project
from sys_mgr.models import User,Space
from django.utils import timezone

class TicketType(models.Model):
	name = models.CharField("类型名", max_length=256)
	code = models.CharField("代码", max_length=64, blank=True, null=True)
	description = models.TextField("类型描述",  blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = u"工单类型"
		verbose_name_plural = verbose_name


class TicketBindInfo(models.Model):
	type = models.ForeignKey('TicketType', verbose_name="工单类型", on_delete=models.CASCADE,
	                         related_name='ticket_bind_info', blank=True, null=True)
	space = models.ForeignKey('sys_mgr.Space', verbose_name="空间", on_delete=models.CASCADE,
	                          related_name='ticket_bind_info_space')
	service = models.ForeignKey('deploy.Service', verbose_name="服务名", on_delete=models.CASCADE)
	audit_user = models.ForeignKey("sys_mgr.User", verbose_name="审核人员", on_delete=models.CASCADE,
	                               related_name='ticket_bind_info_audit_user', blank=True, null=True)
	execute_user = models.ForeignKey("sys_mgr.User", verbose_name="执行人员", on_delete=models.CASCADE,
	                                 related_name='ticket_bind_info_execute_user', blank=True, null=True)
	test_user = models.ForeignKey("sys_mgr.User", verbose_name="测试人员", on_delete=models.CASCADE,
	                              related_name='ticket_bind_info_test_user', blank=True, null=True)

	def __str__(self):
		return "{0}-{1}-{2}-{3}-{4}".format(self.type,self.space,self.service,self.audit_user,self.execute_user,self.test_user)

	class Meta:
		verbose_name = u"工单绑定信息"
		verbose_name_plural = verbose_name


class Ticket(models.Model):
	number = models.CharField(max_length=64, verbose_name='工单编号', null=True, blank=True)
	type = models.ForeignKey('TicketType', verbose_name="工单类型", on_delete=models.CASCADE, related_name='tickets', blank=True, null=True)
	parent = models.ForeignKey('self', verbose_name="父工单", on_delete=models.CASCADE, related_name='sub_tickets', blank=True, null=True)
	title = models.CharField("说明", max_length=256, null=False, blank=False, default="")
	space = models.ForeignKey('sys_mgr.Space', verbose_name="空间", on_delete=models.CASCADE, related_name='tickets_space')
	service = models.ForeignKey('deploy.Service', verbose_name="服务名", on_delete=models.CASCADE, default=None)
	vcs_tag = models.CharField("分支或标签", max_length=256,blank=True, null=True)
	test_user = models.ForeignKey("sys_mgr.User", verbose_name="测试人员", on_delete=models.CASCADE, related_name='tickets_test_user', blank=True, null=True)
	test_description = models.TextField("测试备注",  blank=True, null=True)
	audit_user = models.ForeignKey("sys_mgr.User", verbose_name="审核人员", on_delete=models.CASCADE, related_name='tickets_audit_user', blank=True, null=True)
	audit_description = models.TextField("审核意见", blank=True, null=True)
	execute_user = models.ForeignKey("sys_mgr.User", verbose_name="执行人员", on_delete=models.CASCADE, related_name='tickets_execute_user')
	execute_description = models.TextField("发布备注", blank=True, null=True)
	cancel_description = models.TextField("作废说明", blank=True, null=True)
	create_user = models.ForeignKey("sys_mgr.User", verbose_name="创建人员", on_delete=models.CASCADE, related_name='tickets_create_user', blank=True, null=True)
	service_conf = models.TextField("服务配置",  blank=True, null=True)
	db_conf = models.TextField("数据库配置",  blank=True, null=True)
	db_file = models.FileField(upload_to='sql/%Y/%m/%d/', verbose_name="数据库文件",  blank=True, null=True)
	other_conf = models.TextField("其他配置", blank=True, null=True)
	status = models.SmallIntegerField("状态", blank=True, default=0)
	tested_at = models.DateTimeField("测试时间", blank=True, null=True)
	audited_at = models.DateTimeField("审核时间", blank=True, null=True)
	executed_at = models.DateTimeField("执行时间", blank=True, null=True)
	finished_at = models.DateTimeField("完成时间", blank=True, null=True)
	created_at = models.DateTimeField("创建时间", auto_now_add=True)

	def __str__(self):
		return "{0}({1})".format(self.title,self.number)

	def is_need_audit(self):
		return True if self.audit_user else False

	def is_need_test(self):
		return True if self.test_user else False

	def audit_approved(self):
		return True if self.status == 11 else False

	def test_approved(self):
		return True if self.status == 31 else False

	def create_update_info(self):
		if self.audit_user:
			self.status = 10
		else:
			self.status = 20
		self.save()

	def audit_update_info(self):
		if self.status == 11:
			self.status = 20
		self.audited_at = timezone.now()
		self.save()

	def execute_update_info(self):
		self.executed_at = timezone.now()
		if self.test_user:
			self.status = 30
		else:
			self.status = 40
			self.finished_at = timezone.now()
		self.save()




	class Meta:
		verbose_name = u"工单"
		verbose_name_plural = verbose_name

