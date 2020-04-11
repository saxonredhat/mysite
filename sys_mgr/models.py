from django.db import models


class User(models.Model):
	username = models.CharField(max_length=64, unique=True)
	password = models.CharField(max_length=128)
	roles = models.ManyToManyField("Role")
	status = models.SmallIntegerField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.username

	def get_perm_url_list(self):
		_perm_url_list=[]
		for role in self.roles.all():
			for permission in role.permissions.all():
				_perm_url_list.append(permission.url)
		return _perm_url_list

	class Meta:
		verbose_name = u"用户"
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
	users = models.ManyToManyField("User")

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = u"空间"
		verbose_name_plural = verbose_name
