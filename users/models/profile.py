# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from martor.models import MartorField
import sys

GENDER_CHOICES = (
    (0, '男'),
    (1, '女'),
    (2, '保密')
)


def UserDesc(instance, filename):
    return "user/{0}/{1}".format(instance.user.id, filename)


@python_2_unicode_compatible
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(verbose_name=u'姓名', max_length=16, default='', blank=True, null=False)
    id_no = models.CharField(verbose_name=u'身份证号码', blank=True, default='', max_length=20, null=False)
    gender = models.IntegerField(verbose_name=u'性别', choices=GENDER_CHOICES, default='2',
                                 blank=False)
    phone = models.CharField(verbose_name=u'手机号码', max_length=20, default='', blank=True, null=False)
    avatar = models.ImageField(verbose_name=u'头像', upload_to=UserDesc, blank=True)
    occupation = models.CharField(verbose_name=u"工作类型", default=u"保密", max_length=20)
    details = MartorField(verbose_name=u'个人介绍', default='', max_length=sys.maxsize)
    details_cn = MartorField(verbose_name=u'个人介绍', default='', max_length=sys.maxsize)

    def __str__(self):
        return self.name


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()


post_save.connect(create_user_profile, sender=User)
