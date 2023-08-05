# -*- coding:utf-8 -*-
__author__ = 'bee'

from django import forms
from django.contrib.auth.models import User, Group

from .models import UserProfile, UserProfileParentRelation, UserClass, UserLeaveRecord, USER_LEAVE_TYPE_CHOICES, \
    UserLevel, UserLevelUpRecord
from django.forms.models import inlineformset_factory
from .validators import user_sn_validator
from bee_django_richtext.custom_fields import RichTextFormField, RichtextWidget


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name"]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['start_date']


profile_inline_formset = inlineformset_factory(User, UserProfile, form=UserProfileForm, can_delete=False)


class UserAvatarForm(forms.ModelForm):
    avatar = forms.FileField(label='')

    class Meta:
        model = UserProfile
        fields = ['avatar']


class UserSearchForm(forms.Form):
    status_list = ((0, '全部'), (1, '正常'), (999, '请假'), (2, '暂停'), (3, '禁用'))
    status = forms.ChoiceField(choices=status_list, label='状态', required=False)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), label='用户组', required=False)
    student_id = forms.CharField(label='学号', required=False)
    first_name = forms.CharField(label='用户姓名', required=False)
    start_expire_date = forms.CharField(label='结课日期', required=False)
    end_expire_date = forms.CharField(label='至', required=False)

    # class Meta:
    #     model = User
    #     fields = ["student_id","first_name"]


class UserProfileParentsForm(forms.Form):
    parent_queryset = User.objects.filter(groups__name__in=UserProfile.get_parent_groupname_list())
    parent = forms.ModelChoiceField(queryset=parent_queryset, label='家长助教', required=False)
    # class Meta:
    #     model = UserProfileParentRelation
    #     fields = ['parent']


class UserProfileUpdateClassForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["user_class"]


class UserProfileWxServicBindForm(forms.Form):
    username = forms.CharField(label='用户名', required=True)
    password = forms.CharField(label='密码', required=True, widget=forms.PasswordInput())
    # class Meta:
    #     model = User
    #     fields = ["username", "password"]


class UserClassForm(forms.ModelForm):
    class Meta:
        model = UserClass
        fields = ["name", 'assistant', 'lecturer', 'agent', "status"]

    def __init__(self, request_user, *args, **kwargs):
        super(UserClassForm, self).__init__(*args, **kwargs)
        # 助教
        assistant_queryset = request_user.get_student_list().filter(
            groups__name__in=UserProfile.get_assistant_groupname_list())
        assistant = forms.ModelChoiceField(queryset=assistant_queryset, label='助教', required=False)
        self.fields['assistant'] = assistant
        # 讲师
        lecturer_queryset = request_user.get_student_list().filter(
            groups__name__in=UserProfile.get_lecturer_groupname_list())
        lecturer = forms.ModelChoiceField(queryset=lecturer_queryset, label='讲师', required=False)
        self.fields['lecturer'] = lecturer
        # 客服
        agent_queryset = request_user.get_student_list().filter(groups__name__in=UserProfile.get_agent_groupname_list())
        agent = forms.ModelChoiceField(queryset=agent_queryset, label='客服', required=False)
        self.fields['agent'] = agent
        if kwargs["instance"]:
            self.initial['assistant'] = kwargs["instance"].assistant
            self.initial['lecturer'] = kwargs["instance"].lecturer
            self.initial['agent'] = kwargs["instance"].agent
        #     self.fields.insert(0,"name")


class UserClassDashBoardSearchForm(forms.ModelForm):
    time = forms.ChoiceField(
        choices=((u"本日", '本日'), (u"昨日", '昨日'), (u"本周", '本周'), (u"上周", '上周'), (u"本月", '本月'), (u"上月", '上月')), label='时间',
        required=True)
    class_name = forms.CharField(label='班级名称', required=False)

    class Meta:
        model = UserClass
        fields = ['time', "status", "class_name"]


class UserClassSearchForm(forms.Form):
    status = forms.ChoiceField(choices=((0, '全部'), (1, '正常'), (2, "已结业"),), required=False, label='状态')
    class_name = forms.CharField(label='班级名称', required=False)
    assistant_name = forms.CharField(label='助教姓名', required=False)
    lecturer_name = forms.CharField(label='讲师姓名', required=False)
    agent_name = forms.CharField(label='客服姓名', required=False)


class UserGroupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['groups']


class UserSNForm(forms.ModelForm):
    sn = forms.CharField(label='缦客号', validators=[user_sn_validator])

    class Meta:
        model = UserProfile
        fields = ['sn']


# 请假/延期
class UserLeaveRecordForm(forms.ModelForm):
    type_choices = ((1, "请假"), (3, "延期"))
    type = forms.ChoiceField(choices=type_choices, label='类型')

    class Meta:
        model = UserLeaveRecord
        fields = ['type', "start", "end", "info"]


# 请假/延期
class UserLeaveRecordCancelForm(forms.ModelForm):
    type_choices = ((2, "销假"),)
    type = forms.ChoiceField(choices=type_choices, label='类型')

    class Meta:
        model = UserLeaveRecord
        fields = ['type', "start", "info"]


# 用户升级
# 学生/助教，升级为助教/讲师
class UserLevelCreateForm(forms.ModelForm):
    before_group_list = UserProfile.get_student_groupname_list() + UserProfile.get_assistant_groupname_list()
    after_group_list = UserProfile.get_assistant_groupname_list() + UserProfile.get_lecturer_groupname_list()
    # before_group = forms.ModelChoiceField(label='升级前用户组',
    #                                       queryset=Group.objects.filter(name__in=before_group_list))
    before_group = forms.ModelMultipleChoiceField(label='升级前用户组',
                                                  queryset=Group.objects.filter(name__in=before_group_list))
    after_group = forms.ModelChoiceField(label='升级后用户组',
                                         queryset=Group.objects.filter(name__in=after_group_list))

    class Meta:
        model = UserLevel
        fields = ['title', "number", "before_group", 'after_group', 'req']


class UserLevelUpdateForm(UserLevelCreateForm):
    class Meta:
        model = UserLevel
        fields = ["number", "before_group", 'after_group', 'req']


class UserLevelUpRecordCreateForm(forms.ModelForm):
    class Meta:
        model = UserLevelUpRecord
        fields = ["level"]


class UserLevelUpRecordUpdateForm(forms.ModelForm):
    result = forms.CharField(label='处理结果', required=False, help_text='(非必填)')

    class Meta:
        model = UserLevelUpRecord
        fields = ["status", 'result']


class CustomUserLevelUpRecordApplyForm(forms.ModelForm):
    class Meta:
        model = UserLevelUpRecord
        fields = []

    def __init__(self, *args, **kwargs):
        super(CustomUserLevelUpRecordApplyForm, self).__init__(*args, **kwargs)
        record = self.instance
        if record:
            if record.can_apply():
                self.fields['application'] = RichTextFormField(label='申请内容', required=True,
                                                               widget=RichtextWidget(app_name='bee_django_user',
                                                                                     model_name='UserLevelUpRecord',
                                                                                     img=True))
                self.initial['application'] = kwargs["instance"].application
        if record.can_supply():
            self.fields['supplement'] = RichTextFormField(label='补充内容', required=True,
                                                          widget=RichtextWidget(app_name='bee_django_user',
                                                                                model_name='UserLevelUpRecord',
                                                                                img=True))
            self.initial['supplement'] = kwargs["instance"].supplement


class UserLevelUpRecordSearchForm(forms.ModelForm):
    name = forms.CharField(label='学生姓名', required=False)
    title = forms.CharField(label='级别标题', required=False)

    class Meta:
        model = UserLevelUpRecord
        fields = ["status", 'name', 'title']


class UserPermisionUpdateForm(forms.Form):
    has_permission = forms.BooleanField(label=u"是否拥有该权限", required=False)


class PermissionSearchForm(forms.Form):
    name = forms.CharField(label=u"权限名称", required=False)
