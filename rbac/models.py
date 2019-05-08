from django.db import models


class Menu(models.Model):
    title = models.CharField('一级菜单', max_length=32)
    weight = models.IntegerField('权重',default=0)
    icon = models.CharField('图标', max_length=32)

    def __str__(self):
        return self.title


class Permission(models.Model):
    url = models.CharField('URL地址', max_length=128)
    title = models.CharField('标题', max_length=108)
    is_menu = models.ForeignKey('Menu', blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True)
    url_name = models.CharField('url别名', max_length=32, unique=True)

    class Meta:
        verbose_name = '权限'
        verbose_name_plural = '所有权限'

    def __str__(self):
        return self.title


class Role(models.Model):
    name = models.CharField('角色名称', max_length=32)
    permission = models.ManyToManyField('Permission', verbose_name='角色所拥有的权限', blank=True)

    class Meta:
        verbose_name_plural = '所有角色'

    def __str__(self):
        return self.name


class User(models.Model):
    # name = models.CharField('用户名', max_length=32)
    # pwd = models.CharField('密码', max_length=32)
    roles = models.ManyToManyField(Role, verbose_name='用户的角色', blank=True)

    class Meta():
        verbose_name_plural = '所有用户'
        abstract=True

