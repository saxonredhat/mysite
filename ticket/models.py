from django.db import models
from deploy.models import Project
from sys_mgr.models import User,Space


class TicketType(models.Model):
	name = models.CharField("类型名", max_length=256)
	description = models.TextField("类型描述",  blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = u"工单类型"
		verbose_name_plural = verbose_name


class Ticket(models.Model):
	number = models.CharField(max_length=64, verbose_name='工单编号', null=True, blank=True)
	type = models.ForeignKey('TicketType', verbose_name="工单类型", on_delete=models.CASCADE, related_name='tickets', blank=True, null=True)
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
		return self.title

	class Meta:
		verbose_name = u"工单"
		verbose_name_plural = verbose_name

