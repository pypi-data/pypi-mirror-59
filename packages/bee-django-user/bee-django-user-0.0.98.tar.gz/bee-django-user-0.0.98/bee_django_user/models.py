# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime, pytz, json, calendar, hashlib, math
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.apps import apps
from django.conf import settings
from dss.Serializer import serializer
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.utils.timezone import localtime
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.db import transaction

from bee_django_crm.models import PreUser
from .signals import update_user_expire_signal, create_user_signal, add_user_class_remove_record, \
    update_user_levelup_record
from .dt import LOCAL_TIMEZONE


# Create your models here.


# def get_crm_preuser():
#     if settings.CRM_PREUSER:
#         return settings.CRM_PREUSER
#     return None


# 用户，扩展的user
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    student_id = models.IntegerField(verbose_name='学号', unique=True, null=True)  # 拼接成用户名
    sn = models.IntegerField(verbose_name='统一缦客号', unique=True, null=True, help_text='只需填写数字')  # 各项目统一使用
    room_id = models.CharField(max_length=180, verbose_name='习琴室ID', null=True, blank=True)  # cc
    gensee_room_id = models.CharField(max_length=180, verbose_name='直播间ID', null=True, blank=True)  # gensee
    user_class = models.ForeignKey('bee_django_user.UserClass', verbose_name='用户班级', on_delete=models.SET_NULL,
                                   null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True, verbose_name='开课日期')
    expire_date = models.DateTimeField(null=True, blank=True, verbose_name='结课日期')
    preuser = models.OneToOneField(settings.CRM_PREUSER, verbose_name='crm用户', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = ProcessedImageField(null=True, blank=True, verbose_name='头像', upload_to='avatars',
                                 processors=[ResizeToFill(50, 50)],
                                 format='JPEG')
    is_pause = models.BooleanField(default=False, blank=True, verbose_name='暂停')
    wxapp_openid = models.CharField(max_length=180, verbose_name='微信小程序open id', blank=True, null=True)  # 微信小程序
    wxservice_openid = models.CharField(max_length=180, null=True, blank=True)  # 微信服务号
    parents = models.ManyToManyField(to='UserProfile', through='UserProfileParentRelation')

    live_mins = models.IntegerField(default=0, verbose_name='直播时长')  # 单位分钟

    class Meta:
        db_table = 'bee_django_user_profile'
        app_label = 'bee_django_user'
        ordering = ['-created_at']
        permissions = (
            ('can_manage', '可以访问后台管理'),
            ('can_change_user_group', '可以修改用户组'),
            ('can_change_user_sn', '可以修改sn号'),
            ('can_change_user_status', '可以修改用户状态'),
            ('can_change_user_parent', '可以修改用户的家长助教'),
            ('reset_user_password', '可以重置用户密码'),
            ('view_all_users', '可以查看所有用户'),
            ('view_manage_users', '可以查看管理的用户'),
            ('view_teach_users', '可以查看教的用户'),
            ('view_child_users', '可以查看亲子用户'),
            ('can_create_user_room', '可以开启直播间'),
        )

    def __unicode__(self):
        if self.user:
            return self.user.first_name
        else:
            return "userprofile:" + self.id.__str__()

    def to_json(self):
        result = serializer(data=self, output_type='json', datetime_format='string', include_attr=(
            'user_id', "student_id", "sn", "room_id", "user_class", "start_date", "expire_date", "preuser", "is_pause"))
        result_dict = json.loads(result)
        result_dict["username"] = self.user.username
        result_dict["name"] = self.user.first_name
        result_dict["days"] = self.get_expire_days()
        result_dict["is_unlimited"] = self.user.is_unlimited()
        result_dict["get_sn"] = self.get_sn()
        result_dict["coin"] = self.user.get_coin_count()
        result_dict["avatar"] = self.user.get_user_profile_image()
        # 腾讯推流链接
        # https://cloud.tencent.com/document/product/267/32735
        if hasattr(settings, "TENCENT_CONFIG") and self.user.userprofile.is_pause == False:
            # if "tencent" in  settings.COURSE_LIVE_PROVIDER_LIST:
            _datetime = timezone.now() + datetime.timedelta(days=1)
            timestamp = calendar.timegm(_datetime.utctimetuple())
            txTime = hex(timestamp)[2:]
            m = hashlib.md5()
            m.update(settings.TENCENT_CONFIG.live_key + self.user.username + txTime)
            txSecret = m.hexdigest()
            # print(txSecret)
            result_dict["live_push_stream_param"] = "txSecret=" + txSecret + "&txTime=" + txTime
        else:
            result_dict["live_push_stream_param"] = ""
        return json.dumps(result_dict)

    def has_group(self, group_name):
        group_name_list = []
        for group in self.user.groups.all():
            group_name_list.append(group.name)
        print(group_name_list)
        if group_name in group_name_list:
            return True
        return False

    @classmethod
    def fix_cc_room_id(cls):
        try:
            from bee_django_course.cc import create_room
            for e in cls.objects.all():
                if not e.room_id:
                    room_id = create_room(e.preuser.name + '的直播间')
                    if room_id:
                        e.room_id = room_id
                        e.save()
        except:
            return

    @classmethod
    def init_sn(cls, start=0):
        user_profile_list = cls.objects.all().order_by('student_id')
        for user_profile in user_profile_list:
            user_profile.sn = UserSN.get_next_sn(start)
            user_profile.save()
            start += 1
        return

    def get_sn(self):
        if self.sn:
            return "MK" + self.sn.__str__()
        return ''

    @classmethod
    def get_max_student_id(cls):
        user_profile_list = cls.objects.filter(student_id__isnull=False).order_by("-student_id")
        if user_profile_list.exists():
            max_student_id = user_profile_list.first().student_id

        else:
            max_student_id = 0
        return max_student_id

    @classmethod
    def get_max_sn(cls):
        sn_list = UserSN.objects.filter(is_used=True).order_by('start')
        if sn_list.exists():
            _sn = sn_list.first()
        else:
            return None
        end = _sn.end
        user_profile_list = UserProfile.objects.filter(sn__isnull=False, sn__lte=end).order_by("-sn")
        if user_profile_list.exists():
            max_sn = user_profile_list.first().sn
        else:
            max_sn = 0
        return max_sn

    # 获取结课倒计时天数
    def get_expire_days(self):
        expire_date = self.expire_date
        if expire_date:
            now = timezone.now()
            days = (expire_date - now).days
        else:
            days = None
        return days

    def get_expire_date_str(self, timezone=False):
        if self.expire_date:
            expire_date = localtime(self.expire_date)
            if timezone:
                return expire_date.strftime("%Y-%m-%d %H:%M:%S%z")
            else:
                return expire_date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return ''

    # 助教用户组
    @classmethod
    def get_assistant_groupname_list(cls):
        return ['助教']

    # 客服用户组
    @classmethod
    def get_agent_groupname_list(cls):
        return ['客服']

    # 讲师用户组
    @classmethod
    def get_lecturer_groupname_list(cls):
        return ['讲师']

    # 学生用户组
    @classmethod
    def get_student_groupname_list(cls):
        return ['亲子学生', '学生']

    # 家长助教用户组
    @classmethod
    def get_parent_groupname_list(cls):
        return ['家长助教']

    # 亲子学生用户组
    @classmethod
    def get_child_groupname_list(cls):
        return ['亲子学生']

    # 获取班级列表
    def get_class_list(self):
        all_classes = UserClass.objects.all()
        if self.user.has_perm("bee_django_user.view_all_classes"):
            return all_classes
        # 客服
        if self.is_role("agent"):
            filter1 = Q(agent__userprofile=self)
        else:
            filter1 = Q(pk=None)
        # 讲师
        if self.is_role("lecturer"):
            filter2 = Q(lecturer__userprofile=self)
        else:
            filter2 = Q(pk=None)
        # 助教
        if self.is_role("mentor"):
            filter3 = Q(assistant__userprofile=self)
        else:
            filter3 = Q(pk=None)
        classes = all_classes.filter(filter1 | filter2 | filter3).distinct()
        return classes

    # 获取用户的助教
    def get_mentor(self):
        if self.user_class:
            return self.user_class.assistant
        else:
            return None

    # 获取用户的讲师
    def get_lecturer(self):
        if not self.user_class:
            return None
        return self.user_class.lecturer

    # 获取用户的客服
    def get_agent(self):
        if not self.user_class:
            return None
        return self.user_class.agent

    # 检查user的身份，是否是客服/讲师/助教/亲子家长/学生/亲子学生
    # _type值：agent/lecturer/mentor/parent/student/clild
    def is_role(self, _type):
        group_name_list = None
        if _type == 'agent':
            group_name_list = self.get_agent_groupname_list()
        elif _type == 'lecturer':
            group_name_list = self.get_lecturer_groupname_list()
        elif _type == 'mentor':
            group_name_list = self.get_assistant_groupname_list()
        elif _type == 'parent':
            group_name_list = self.get_parent_groupname_list()
        elif _type == 'student':
            group_name_list = self.get_student_groupname_list()
        elif _type == 'clild':
            group_name_list = self.get_child_groupname_list()
        if not group_name_list:
            return False
        groups = self.user.groups.filter(name__in=group_name_list)
        if groups.exists():
            return True
        return False

    # 是否是助教
    def is_assistant(self):
        return self.is_role('mentor')

    # 是否亲子学生
    def is_child(self):
        return self.is_role('clild')

    #
    # def create_cc_room(self):
    #     try:
    #         from bee_django_course.cc import create_room
    #         room=create_room(self.name+"的直播间")
    #         self.room_id=room
    #         self.save()
    #     except:
    #         return
    #
    # def create_gensee_room(self):
    #     try:
    #         from bee_django_course.gensee import create_room
    #         room = create_room(self.name+"的直播间")
    #         self.gensee_room_id=room
    #         self.save()
    #     except:
    #         return

    # 创建User
    # type-1:创建普通用户
    # type-2:亲子用户，创建一组账号
    @classmethod
    def create_user(cls, op_user, preuser, type, group_name=None):
        # preuser_id = request.GET["preuser_id"]
        # preuser_fee_id = request.GET["preuser_fee_id"]
        if not op_user.has_perm('bee_django_user.add_userprofile'):
            return None, None, 1, "没有权限"
        try:
            user_profile = preuser.userprofile
            if user_profile:
                return None, None, 0, "已添加过用户，审核成功"
        except:
            pass

        new_user, parent_user, error, msg = cls._create_user(preuser, type, group_name)
        if new_user:
            # 发送信号
            create_user_signal.send(sender=User, user=new_user)
        return new_user, parent_user, error, msg

    # 1-普通用户，2-亲子学生/家长一套用户
    @classmethod
    def _create_user(cls, preuser, type, group_name=None):
        user_profile = UserProfile()
        # sn
        max_sn = UserProfile.get_max_sn()
        sn = UserSN.get_next_sn(max_sn)
        if not sn:
            return None, None, 4, '统一缦客号生成错误'
        user_profile.sn = sn

        # 学号
        max_student_id = UserProfile.get_max_student_id()
        user_profile.preuser = preuser
        user_profile.student_id = max_student_id + 1
        # 保存user_profile
        user_profile.save()

        new_user = User.objects.create_user(username=settings.USER_EX_USERNAME + user_profile.student_id.__str__(),
                                            password=settings.USER_DEFAULT_PASSWORD)
        new_user.first_name = user_profile.preuser.name
        new_user.save()
        #
        user_profile.user = new_user
        user_profile.save()

        parent_user = None
        if type == 1:
            if not group_name:
                group_name = '学生'
            try:
                group, is_create = Group.objects.get_or_create(name=group_name)
                new_user.groups.add(group)
            except:
                pass
        elif type == 2:
            # 学生角色
            try:
                group = Group.objects.get(name='亲子学生')
            except:
                group = Group(name='亲子学生')
                group.save()
            new_user.groups.add(group)
            # 再创建一个家长用户
            p_user = User.objects.create_user(
                username=settings.USER_EX_USERNAME + user_profile.student_id.__str__() + "s",
                password=settings.USER_DEFAULT_PASSWORD)
            p_user.first_name = user_profile.preuser.name + "的家长"
            p_user.save()

            p_user_profile = UserProfile()
            p_user_profile.user = p_user
            p_user_profile.save()
            # 家长角色
            try:
                p_group = Group.objects.get(name='家长助教')
                # p_user.groups.add(p_group)
            except:
                p_group = Group(name='家长助教')
                p_group.save()
            p_user.groups.add(p_group)
            # 学生家长对应关系
            r = UserProfileParentRelation()
            r.student = new_user.userprofile
            r.parent = p_user.userprofile
            r.save()
            parent_user = p_user

        return new_user, parent_user, 0, '添加用户成功'


class UserProfileParentRelation(models.Model):
    student = models.ForeignKey(UserProfile, related_name='student', verbose_name='学生')
    parent = models.ForeignKey(UserProfile, related_name='parent', verbose_name='家长')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student

    class Meta:
        db_table = 'bee_django_user_parent'
        app_label = 'bee_django_user'
        ordering = ['pk']


class UserSN(models.Model):
    start = models.IntegerField(verbose_name='起', unique=True)
    end = models.IntegerField(verbose_name='止', unique=True)
    is_used = models.BooleanField(verbose_name='是否正在使用', default=False)

    def __str__(self):
        return self.start.__str__() + '-' + self.end.__str__()

    class Meta:
        db_table = 'bee_django_user_sn'
        app_label = 'bee_django_user'
        ordering = ['start']

    @classmethod
    def get_next_sn(cls, sn=0):
        if sn == None:
            return None
        new_sn = sn + 1
        sn_list = cls.objects.filter(is_used=True).order_by('start')
        if not sn_list.exists():
            return None
        i = sn_list.first()

        if new_sn <= i.start:
            new_sn = i.start
        elif i.start < new_sn < i.end:
            pass
        elif new_sn == i.end:
            # 开启下一区间
            next_list = cls.objects.filter(is_used=False).order_by('start')
            if next_list.exists():
                next = next_list.first()
                next.is_used = True
                next.save()
            # 关闭当前区间
            i.is_used = False
            i.save()

        else:
            return None
        return new_sn

        # @receiver(post_save, sender=UserProfile)
        # def create_user(sender, **kwargs):
        #     user_pofile = kwargs['instance']
        #     if not kwargs['created']:
        #         return
        #
        #     preuser = user_pofile.preuser
        # contract_list = preuser.preusercontract_set.filter(preuser__preusercontract__contract__type==2)
        # if contract_list.ex

        # 普通合同，正常创建账号

        # 亲子合同，创建正式账号外，再创建家长助教账号S

        # if user_pofile.preuser
        # user = User.objects.create_user(username=settings.USER_EX_USERNAME + user_pofile.student_id.__str__(),
        #                                 password=settings.USER_DEFAULT_PASSWORD)
        # user.first_name = user_pofile.preuser.name
        # user.save()
        # #
        # user_pofile.user = user
        # user_pofile.save()
        # try:
        #     group = Group.objects.get(name='学生')
        #     user.groups.add(group)
        # except Exception as e:
        #     print(e)

        # 发送信号
        # create_user_signal.send(sender=User, user=user)

        # return


# @receiver(post_save, sender=User)
# def create_user_profile(sender, **kwargs):
#     user = kwargs['instance']
#     if kwargs['created']:
#         user_profile_list = UserProfile.objects.all().order_by("-student_id")
#         if user_profile_list.count() >= 1:
#             max_student_id = user_profile_list.first().student_id
#         else:
#             max_student_id = 0
#         user_profile = UserProfile(user=user)
#         user_profile.student_id = max_student_id + 1
#         user_profile.save()
#     return
# 如果有crm，则创建并关联crm用户
# res = apps.is_installed("bee_django_crm")
# if not res:
#     return
# try:
#     from bee_django_crm.models import PreUser
#     preuser = PreUser(user=user)
#     preuser.save()
# except:
#     return

USER_LEAVE_TYPE_CHOICES = ((1, '请假'), (2, "请假有销假"), (3, '延期'), (4, '提前'))


class UserLeaveRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='leave_user')
    type = models.IntegerField(choices=USER_LEAVE_TYPE_CHOICES, default=1, verbose_name='类型')
    start = models.DateTimeField(null=True, blank=True, verbose_name='开始日期')
    end = models.DateTimeField(null=True, blank=True, verbose_name='结束日期')
    old_expire = models.DateTimeField(blank=True, verbose_name='原结课日期', null=True)
    new_expire = models.DateTimeField(blank=True, verbose_name='新结课日期')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='create_user')
    created_at = models.DateTimeField(default=timezone.now)
    is_check = models.BooleanField(default=False, verbose_name='通过审核')
    check_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='check_user')
    check_at = models.DateTimeField(null=True)
    info = models.TextField(verbose_name='备注', null=True, blank=True)

    class Meta:
        db_table = 'bee_django_user_leave_record'
        app_label = 'bee_django_user'
        ordering = ['-created_at']
        permissions = (
            ('update_type_cancel', "可以销假"),
            ('change_check', '可以审核用户的请假'),
        )

    def __str__(self):
        return self.pk.__str__()

    def get_type(self):
        if not self.type:
            return ""
        for g in USER_LEAVE_TYPE_CHOICES:
            if self.type == g[0]:
                return g[1]
        return ""

    # 审核请假记录后，自动更新用户的结课日期
    def update_user_expire(self):
        if self.is_check == True:
            user = self.user
            user.userprofile.expire_date = self.new_expire
            user.userprofile.save()
        return


# 学生请假状态表
class UserLeaveStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    status = models.IntegerField(default=0)  # 1请假中，2正常-请假期未到，3正常-请假期已处理完成
    leave_start = models.DateTimeField(null=True, blank=True, verbose_name='请假开始日期')
    leave_end = models.DateTimeField(null=True, blank=True, verbose_name='请假结束日期')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    record = models.ForeignKey(UserLeaveRecord, null=True)  #

    class Meta:
        db_table = 'bee_django_user_leave_status'
        app_label = 'bee_django_user'
        ordering = ['-created_at']

    def __str__(self):
        return self.user.username + ",status:" + self.status.__str__()

    def update_status(self):
        now = timezone.now()
        # 请假中的学生
        if self.status == 1:
            if self.leave_end <= now:
                self.status = 3
                self.save()
        # 新添加的学生，或未到请假期的学生
        elif self.status in [0, 2]:
            if self.leave_start <= now:
                self.status = 1
                self.save()
            if self.leave_end <= now:
                self.status = 3
                self.save()
        return

    def get_status(self):
        if self.status == 1:
            return '请假中'
        elif self.status == 2:
            return '请假期未到'
        elif self.status == 3:
            return '请假期已处理完成'

        return ''


# 审核请假记录后
# 1.自动更新用户的结课日期
# 2.自动更新到用户状态表
# 3.发送信号，创建一条足迹
@receiver(post_save, sender=UserLeaveRecord)
def update_user_expire(sender, **kwargs):
    record = kwargs['instance']
    if kwargs['created'] == False and record.is_check == True:
        # 自动更新用户的结课日期
        user = record.user
        user.userprofile.expire_date = record.new_expire
        user.userprofile.save()
        # 发送信号
        update_user_expire_signal.send(sender=UserLeaveRecord, leave_record=record)
        # 请假
        if record.type == 1:
            n = UserLeaveStatus()
            n.user = record.user
            n.leave_start = record.start
            n.leave_end = record.end
            n.record = record
            n.save()
            # 更新状态
            n.update_status()
        # 销假
        elif record.type == 2:
            try:
                n = UserLeaveStatus.objects.get(record=record)
            except:
                return
            n.leave_start = record.start
            n.leave_end = record.end
            n.save()
            # 更新状态
            n.update_status()
    return


# 班级
class UserClass(models.Model):
    name = models.CharField(max_length=180, verbose_name='班级名称', unique=True, help_text='不能和已有班级重名')
    assistant = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assistant_user', verbose_name='助教', null=True,
                                  blank=True)
    lecturer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='讲师', null=True, blank=True,
                                 related_name='lecturer_user')  # 讲师
    agent = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='agent_user', null=True, on_delete=models.SET_NULL,
                              blank=True)  # 客服
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=((1, '正常'), (2, "已结业"),), verbose_name='班级状态', default=1, blank=True)
    passed_at = models.DateTimeField(null=True, verbose_name='结业时间')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'bee_django_user_class'
        app_label = 'bee_django_user'
        ordering = ['-created_at']
        permissions = (
            ('view_all_classes', '可以查看所有班级'),
            ('view_manage_classes', '可以查看管理的班级'),
            ('view_teach_classes', '可以查看教的班级'),
        )

    def get_students(self):
        user_profile_list = self.userprofile_set.all()
        user_list = User.objects.filter(userprofile__in=user_profile_list)
        return user_list

    def get_teacher_info(self, separator='。'):
        _list = []
        if self.assistant:
            _list.append("助教：" + self.assistant.first_name)
        if self.lecturer:
            _list.append("讲师：" + self.lecturer.first_name)
        if self.agent:
            _list.append("客服：" + self.agent.first_name)
        return separator.join(_list)

    def get_status(self):
        if self.status == 1:
            return '正常'
        if self.status == 2:
            return '已结业'

    def get_student_class_remove_record(self, start_dt=None, end_dt=None):
        records = UserClassRemoveRecord.objects.filter(Q(old_class=self) | Q(new_class=self))
        if start_dt:
            min_start_dt = start_dt - datetime.timedelta(days=31)
            records = records.filter(created_at__gte=min_start_dt)
        if end_dt:
            max_end_dt = end_dt + datetime.timedelta(days=31)
            records = records.filter(created_at__lte=max_end_dt)
        return records


class UserClassRemoveRecord(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='student', verbose_name='学生')  # 学生
    old_class = models.ForeignKey(UserClass, related_name='old_class', verbose_name='原班级', null=True)  # 原班级
    new_class = models.ForeignKey(UserClass, related_name='new_class', verbose_name='新班级', null=True)  # 新班级
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='created_by', verbose_name='操作人')

    class Meta:
        db_table = 'bee_django_user_class_remove_record'
        app_label = 'bee_django_user'
        ordering = ['-created_at']
        permissions = (
            ('view_user_class_remove_records', 'view_user_class_remove_records'),
        )

    def __unicode__(self):
        return self.pk.__str__()

    def get_info(self, teacher_info=None):
        if not self.old_class:
            old_class_info = '无'
        else:
            old_class_info = self.old_class.name
            if teacher_info:
                old_class_info += "。" + self.old_class.get_teacher_info()
        if not self.new_class:
            new_class_info = '无'
        else:
            new_class_info = self.new_class.name
            if teacher_info:
                new_class_info += "。" + self.new_class.get_teacher_info()
        return "【" + self.created_by.first_name + "】于【" + self.created_at.astimezone(LOCAL_TIMEZONE).strftime(
            "%Y-%m-%d %H:%M:%S") + "】操作：原班级【" + old_class_info + "】->【" + new_class_info + "】"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(UserClassRemoveRecord, self).save(force_insert, force_update, using, update_fields)
        # 发送信号
        add_user_class_remove_record.send(sender=UserClassRemoveRecord, user=self.student,
                                          info=self.get_info(teacher_info=True))
        return


# 助教系统升级
class UserLevel(models.Model):
    title = models.CharField(max_length=180, verbose_name='标题')
    number = models.IntegerField(verbose_name='顺序', default=0)
    before_group = models.ManyToManyField(Group, verbose_name='可升级用户组', help_text='（可多选）',
                                          related_name='user_before_group')
    after_group = models.ForeignKey(Group, verbose_name='升级后的用户组', help_text='（不可多选）', related_name='user_after_group',
                                    null=True, blank=True)
    req = models.TextField(verbose_name='申请要求', null=True, blank=True)

    class Meta:
        db_table = 'bee_django_user_level'
        app_label = 'bee_django_user'
        ordering = ['number']
        permissions = (
            ('view_level_list', '可以查看用户升级列表'),
        )

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('bee_django_user:level_detail', kwargs={'pk': self.pk})


USER_LEVEL_UP_STATUS_CHOICES = ((-1, "未申请"), (-2, "已申请"), (1, '通过'), (2, '未通过'), (3, '关闭'), (4, '已提交补充资料'))


class UserLevelUpRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bee_django_level_up_user')
    level = models.ForeignKey("bee_django_user.UserLevel", related_name='bee_django_user_level', null=True,
                              on_delete=models.SET_NULL, verbose_name='升级标题')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=USER_LEVEL_UP_STATUS_CHOICES, null=True, verbose_name="状态", blank=True,
                                 default=-1)
    application = models.TextField(verbose_name='申请内容', null=True, blank=True)
    supplement = models.TextField(verbose_name='补充资料', null=True, blank=True)
    history = models.TextField(verbose_name='历史记录', null=True, blank=True)
    info = models.TextField(verbose_name='其他', null=True, blank=True)

    # result = models.CharField(max_length=180, null=True, blank=True, verbose_name='处理意见')

    class Meta:
        db_table = 'bee_django_user_level_up_record'
        app_label = 'bee_django_user'
        ordering = ['-created_at']
        permissions = (
            ('view_all_level_up_records', '可以查看用户升级列表'),
        )

    def get_status_str(self):
        if self.status == -1:
            return '未申请'
        if self.status == -2:
            return '已申请'
        if self.status == 1:
            return '已通过'
        if self.status == 2:
            return '未通过'
        if self.status == 3:
            return '关闭'
        if self.status == 4:
            return '已提交补充资料'

    # 可以提交申请的状态
    def can_apply(self):
        if self.status in [-1]:
            return True

    # 可以提交补充资料的状态
    def can_supply(self):
        if self.status in [1]:
            return True

    # 可以操作的状态
    def can_change_status(self):
        if self.status in [-1, -2, 2, 3]:
            return True

    # 变更状态
    # _type：create/apply/pass/reject/close/open/supply
    @transaction.atomic
    def chenge_status(self, op_user, _type, result=None):
        if _type == 'create':
            self.status = -1
            status_str = '创建'
        elif _type == 'apply':
            self.status = -2
            status_str = '提交申请'
        elif _type == 'pass':
            self.status = 1
            status_str = '通过'
            res = UserLevelUpRecord.check_user_group(self.user, self.level.before_group.all())
            if not res:
                return
            self.change_user_group()
        elif _type == 'reject':
            self.status = 2
            status_str = '驳回'
        elif _type == 'close':
            self.status = 3
            status_str = '关闭'
        elif _type == 'open':
            self.status = -1
            status_str = '重新开放'
        elif _type == 'supply':
            self.status = 4
            status_str = '提交补充内容'
        else:
            return
        if not self.history:
            self.history = ''
        self.history += '<p>由【' + op_user.first_name + "】于【" + timezone.localtime().strftime(
            "%Y-%m-%d %H:%M:%S") + "】" + status_str
        if result:
            self.history += '。处理意见：' + result
        self.save()
        if _type in ["pass", "reject", "close", "open"]:
            # 发送信号
            update_user_levelup_record.send(sender=self.__class__, user_levelup_record=self, title=status_str)
        return

    # 通过后更换用户组
    def change_user_group(self):
        if not self.level.after_group:
            return
        group = self.level.after_group
        self.user.groups.add(group)
        return

    # 添加的时候检查
    @classmethod
    def check_add_user_record(cls, user, level=None):
        user_records = cls.objects.filter(user=user).filter(status__in=[-1, -2, 2, 0])
        if user_records.exists():
            return False, "当前有一个进行中的升级"
        if level:
            before_group = level.before_group.all()
            res = cls.check_user_group(user, before_group)
            if res:
                return True, ''
            else:
                return False, '该用户不属于可升级用户组'
        else:
            return True, ''

    # 检查用户是否属于可升级的用户组
    @classmethod
    def check_user_group(cls, user, groups):
        group_name_list = []
        for g in groups:
            group_name_list.append(g.name)
        group_list = user.groups.filter(name__in=group_name_list)
        if group_list.exists():
            return True
        else:
            return False

    # 获取学生的升级记录
    @classmethod
    def get_user_first_record(cls, user, status_list=None):
        record_list = cls.objects.filter(user=user)
        if status_list:
            record_list = record_list.filter(status__in=status_list)
        if record_list.exists():
            return record_list.first()
        return None


class CustomAuthPermission(models.Model):
    auth_permission = models.OneToOneField(Permission)
    app_title = models.CharField(max_length=180, verbose_name='应用', null=True)
    model_title = models.CharField(max_length=180, verbose_name='模块', null=True)
    codename_title = models.CharField(max_length=180, verbose_name='权限', null=True)
    number = models.IntegerField(verbose_name='顺序', null=True)
    can_edit = models.BooleanField(verbose_name='是否可以编辑', default=False)

    class Meta:
        db_table = 'bee_django_user_permission'
        app_label = 'bee_django_user'
        ordering = ['number']
        permissions = (
            ('can_edit_permission', 'can_edit_permission'),
        )

    def __unicode__(self):
        return self.app_title + ' - ' + self.model_title + ' - ' + self.codename_title


# =================

def get_user(self):
    return self.username + " " + self.first_name


def get_user_name(self):
    return self.first_name


# 学生列表页根据student_id搜索
def get_user_search_link(self):
    ex_link = "/user/list/?id="
    search = self.id.__str__()
    return ex_link + search


# 获取用户的coin数量
def get_coin_count(self):
    try:
        from bee_django_coin.exports import get_user_coin
        coin = get_user_coin(self)
        return coin
    except:
        return 0


# 增加/扣除m币
def add_coin_record(self, reason, identity, coin, count, created_by):
    try:
        from bee_django_coin.exports import add_coin_record as _add_coin_record
        coin = _add_coin_record(self, reason, identity, coin, count, created_by)
        if coin:
            return True
    except:
        return False


User.add_to_class("__unicode__", get_user)
User.add_to_class("get_user_name", get_user_name)
User.add_to_class("get_user_search_link", get_user_search_link)
User.add_to_class("get_coin_count", get_coin_count)
User.add_to_class("add_coin_record", add_coin_record)


# 获取学生是否暂停
def get_is_pause(self):
    if self.userprofile:
        return self.userprofile.is_pause
    return None


User.add_to_class("is_pause", get_is_pause)


# 获取学生状态
def get_user_status(self):
    _str = ''
    if self.userprofile.is_pause == True:
        _str += '（已暂停）'
    if self.is_active == False:
        _str += '（已禁用）'
    return _str


User.add_to_class("get_user_status", get_user_status)


# 获取学生sn
def get_sn(self):
    return self.userprofile.get_sn()


User.add_to_class("get_sn", get_sn)


# 获取学生结课日期
def get_expire_date(self):
    if self.userprofile:
        return self.userprofile.expire_date
    return None


User.add_to_class("get_expire_date", get_expire_date)


# 日志用户的头像地址获取
def get_user_profile_image(self):
    if self.userprofile:
        try:
            avatar = self.userprofile.avatar
            if avatar:
                return avatar.url
            else:
                return None
        except AttributeError:
            return None
    else:
        return None


User.add_to_class('get_user_profile_image', get_user_profile_image)


# 终身缦客
def is_unlimited(self):
    if self.userprofile.expire_date:
        if int(self.userprofile.expire_date.strftime("%Y")) >= 2999:
            return True
    return False


User.add_to_class('is_unlimited', is_unlimited)


# 获取亲子学生
def get_child_users(self):
    return User.objects.filter(userprofile__parents=self.userprofile)


User.add_to_class('get_child_users', get_child_users)


# 获取学生的助教
def get_assistant(self):
    if self.userprofile:
        mentor = self.userprofile.get_mentor()
        return mentor
    else:
        return None


User.add_to_class('get_assistant', get_assistant)


# 获取学生的讲师
def get_lecturer(self):
    if self.userprofile:
        lecturer = self.userprofile.get_lecturer()
        return lecturer
    else:
        return None


User.add_to_class('get_lecturer', get_lecturer)


# 获取学生的客服
def get_agent(self):
    if self.userprofile:
        agent = self.userprofile.get_agent()
        return agent
    else:
        return None


User.add_to_class('get_agent', get_agent)


# 判断menotr是否是user的助教

# 是否是user的助教
def is_user_assistant(self, user):
    if not self.userprofile.is_assistant():
        return False
    mentor = user.get_assistant()
    if mentor == self:
        return True
    return False


User.add_to_class('is_user_assistant', is_user_assistant)


# 重置学生的直播时长
def set_live_mins(self, mins):
    if self.userprofile:
        self.userprofile.live_mins = mins
        self.userprofile.save()
        return True
    return False


User.add_to_class('set_live_mins', set_live_mins)


# ===============
# 根据练习时间获取缦客级别
def get_user_level(self):
    if not self.userprofile:
        return 0
    live_mins = self.userprofile.live_mins
    if not live_mins:
        return 0
    if live_mins < 100:
        return 1
    if live_mins < 200:
        return 2
    level = 2
    practice_time = live_mins / 100
    level += math.log(practice_time, 2)
    return int(level)


User.add_to_class('get_user_level', get_user_level)


# 获取特定的学生列表
def get_student_list(self):
    all_users = User.objects.all().order_by('userprofile__student_id')
    if self.has_perm("bee_django_user.view_all_users"):
        return all_users
    userprofile = self.userprofile
    if not userprofile:
        return User.objects.none()
    # 客服
    if userprofile.is_role("agent"):
        filter1 = Q(userprofile__user_class__agent=self)
    else:
        filter1 = Q(pk=None)
    # 讲师
    if userprofile.is_role("lecturer"):
        filter2 = Q(userprofile__user_class__lecturer=self)
    else:
        filter2 = Q(pk=None)
    # 助教
    if userprofile.is_role("mentor"):
        filter3 = Q(userprofile__user_class__assistant=self)
    else:
        filter3 = Q(pk=None)
    # 家长助教
    if userprofile.is_role("parent"):
        filter4 = Q(userprofile__parents=self)
    else:
        filter4 = Q(pk=None)
    users = all_users.filter(filter1 | filter2 | filter3 | filter4).distinct()

    return users


User.add_to_class('get_student_list', get_student_list)


def get_teacher_list(self, _role):
    if not self.userprofile:
        return User.objects.none()
    if self.has_perm("bee_django_user.view_all_users"):
        all_users = User.objects.all().order_by('userprofile__student_id')
        if _role == 'agent':
            return all_users.filter(groups__name__in=self.userprofile.get_agent_groupname_list())
        if _role == 'lecturer':
            return all_users.filter(groups__name__in=self.userprofile.get_lecturer_groupname_list())
        if _role == 'mentor':
            return all_users.filter(groups__name__in=self.userprofile.get_assistant_groupname_list())

    else:
        user_class_list = self.userprofile.get_class_list()
        if _role == 'agent':
            _list = []
            for user_class in user_class_list:
                _list.append(user_class.agent.id)
            return User.objects.filter(pk__in=_list)
        elif _role == 'lecturer':
            _list = []
            for user_class in user_class_list:
                _list.append(user_class.lecturer.id)
            return User.objects.filter(pk__in=_list)
        elif _role == 'mentor':
            _list = []
            for user_class in user_class_list:
                _list.append(user_class.assistant.id)
            return User.objects.filter(pk__in=_list)


User.add_to_class('get_teacher_list', get_teacher_list)
