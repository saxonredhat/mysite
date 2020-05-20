from django.db import models


class User(models.Model):
	username = models.CharField(max_length=64, unique=True)
	chinese_name = models.CharField(max_length=64,blank=True,null=True, verbose_name="中文名")
	password = models.CharField(max_length=128)
	roles = models.ManyToManyField("Role")
	spaces = models.ManyToManyField("Space")
	position = models.ManyToManyField("Position", verbose_name="职位")
	status = models.SmallIntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.chinese_name if self.chinese_name else self.username

	def get_perm_url_list(self):
		_perm_url_list=[]
		for role in self.roles.all():
			for permission in role.permissions.all():
				_perm_url_list.append(permission.url)
		return _perm_url_list

	class Meta:
		verbose_name = u"用户"
		verbose_name_plural = verbose_name


class Department(models.Model):
	name = models.CharField(max_length=64, verbose_name="部门名", unique=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = u"部门"
		verbose_name_plural = verbose_name


class Position(models.Model):
	name = models.CharField(max_length=64, verbose_name="职位名称", unique=True)
	department = models.ForeignKey("Department", verbose_name="部门", on_delete=models.CASCADE)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = u"职位"
		verbose_name_plural = verbose_name


class Role(models.Model):
	name = models.CharField(max_length=64)
	permissions = models.ManyToManyField("Permission")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = u"角色"
		verbose_name_plural = verbose_name


class Permission(models.Model):
	name = models.CharField(max_length=64)
	url = models.CharField(max_length=200, null=True, blank=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = u"权限"
		verbose_name_plural = verbose_name


class Menu(models.Model):
	name = models.CharField(max_length=64)
	url = models.CharField(max_length=128, null=True, blank=True)
	parent_menu = models.ForeignKey("Menu", null=True, blank=True, on_delete=models.CASCADE)
	icon_name = models.CharField(max_length=32, default='circle')
	seq = models.IntegerField()

	def __str__(self):
		if self.parent_menu is not None:
			return "[ "+self.parent_menu.name+" ]->"+"[ "+self.name+" ]"
		return "[ "+self.name+" ]"

	class Meta:
		verbose_name = u"菜单"
		verbose_name_plural = verbose_name


class Space(models.Model):
	name = models.CharField(max_length=64)
	code = models.CharField(max_length=64, unique=False, default="")

	def __str__(self):
		return "{0}({1})".format(self.name,self.code)

	class Meta:
		verbose_name = u"空间"
		verbose_name_plural = verbose_name
