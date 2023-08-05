# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime, os, csv
from django.shortcuts import render, redirect, reverse, HttpResponse
from django.utils.timezone import localtime
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.db.models import Q, Sum, Count
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.conf import settings
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import AdminPasswordChangeForm
from PIL import Image, ExifTags
from django.contrib.contenttypes.models import ContentType
# from bee_django_crm.models import PreUser
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt

from .decorators import cls_decorator, func_decorator
from .models import UserProfile, UserSN, UserClassRemoveRecord, UserProfileParentRelation, UserClass, UserLeaveRecord, \
    LOCAL_TIMEZONE, \
    UserLevel, UserLevelUpRecord, CustomAuthPermission
from .forms import UserForm, UserProfileParentsForm, UserAvatarForm, UserSearchForm, UserProfileWxServicBindForm, \
    profile_inline_formset, \
    UserClassForm, UserClassDashBoardSearchForm, \
    UserClassSearchForm, UserGroupForm, \
    UserSNForm, UserProfileUpdateClassForm, \
    UserLeaveRecordForm, \
    UserLeaveRecordCancelForm, UserLevelCreateForm, UserLevelUpdateForm, UserLevelUpRecordCreateForm, \
    UserLevelUpRecordUpdateForm, UserLevelUpRecordSearchForm, CustomUserLevelUpRecordApplyForm, UserPermisionUpdateForm, \
    PermissionSearchForm
from .utils import export_csv
from .signals import update_user_active_pause_signal

User = get_user_model()


# Create your views here.
def test(request):
    # a=u.userprofile.is_assistant()
    # print(a)
    # if hasattr(settings,"GENSEE_CONFIG"):
    # print(b)
    #     print(settings.GENSEE_CONFIG.genseeUrl)
    # try:
    #     a=settings.aaa
    #     print('====')
    # except:
    #     print('222')
    from .models import UserClassRemoveRecord
    a = UserClassRemoveRecord.objects.all().first()
    print a.get_info()
    return HttpResponse("OK")


def home_page(request):
    return render(request, 'bee_django_user/home_page.html')


# ========user 学生===========
@method_decorator(cls_decorator(cls_name='UserList'), name='dispatch')
class UserList(ListView):
    model = User
    template_name = 'bee_django_user/user/list.html'
    context_object_name = 'user_list'
    paginate_by = 20
    queryset = None

    def search(self):
        # if self.request.user.has_perm("bee_django_user.view_all_users"):
        #     queryset = User.objects.all().order_by('userprofile__student_id')
        # else:
        #     if self.request.user.has_perm("bee_django_user.view_teach_users"):
        #         filter1 = Q(userprofile__user_class__assistant=self.request.user)
        #     else:
        #         filter1 = Q(pk=None)
        #     if self.request.user.has_perm("bee_django_user.view_child_users"):
        #         filter2 = Q(userprofile__parents=self.request.user.userprofile)
        #     else:
        #         filter2 = Q(pk=None)
        #     queryset = User.objects.filter(filter1 | filter2).order_by('id').distinct()
        queryset = self.request.user.get_student_list()
        id = self.request.GET.get("id")
        status = self.request.GET.get("status")
        student_id = self.request.GET.get("student_id")
        first_name = self.request.GET.get("first_name")
        group_id = self.request.GET.get("group")
        start_expire_date = self.request.GET.get("start_expire_date")
        end_expire_date = self.request.GET.get("end_expire_date")
        if not id in [0, "0", None]:
            queryset = queryset.filter(pk=id)
        if not status in [0, "0", None]:
            if status == "1":
                queryset = queryset.filter(is_active=True, userprofile__is_pause=False).exclude(
                    userleavestatus__status=1)
            elif status == "2":
                queryset = queryset.filter(userprofile__is_pause=True)
            elif status == "3":
                queryset = queryset.filter(is_active=False)
            elif status == "999":
                queryset = queryset.filter(userleavestatus__status=1)
        if student_id:
            queryset = queryset.filter(userprofile__student_id=student_id)
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if group_id:
            queryset = queryset.filter(groups__id__in=[group_id])
        if start_expire_date:
            queryset = queryset.filter(userprofile__expire_date__gte=start_expire_date)
        if end_expire_date:
            queryset = queryset.filter(userprofile__expire_date__lte=end_expire_date)
        self.queryset = queryset
        return self.queryset

    # def get_queryset(self):
    #     queryset = []
    #     if self.request.user.has_perm("bee_django_user.view_all_users"):
    #         queryset = User.objects.all().order_by('id')
    #     elif self.request.user.has_perm("bee_django_user.view_teach_users"):
    #         queryset = User.objects.filter(userprofile__user_class__assistant=self.request.user).order_by('id')
    #     else:
    #         self.queryset=[]
    #         return self.queryset
    #
    #     student_id = self.request.GET.get("student_id")
    #     first_name = self.request.GET.get("first_name")
    #     group_id = self.request.GET.get("group")
    #     if student_id:
    #         queryset = queryset.filter(userprofile__student_id=student_id)
    #     if first_name:
    #         queryset = queryset.filter(first_name__icontains=first_name)
    #     if group_id:
    #         queryset = queryset.filter(groups__id__in=[group_id])
    #     self.queryset=queryset
    #     return self.queryset

    def get_context_data(self, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        status = self.request.GET.get("status")
        student_id = self.request.GET.get("student_id")
        first_name = self.request.GET.get("first_name")
        group = self.request.GET.get("group")
        start_expire_date = self.request.GET.get("start_expire_date")
        end_expire_date = self.request.GET.get("end_expire_date")

        context['search_form'] = UserSearchForm(
            {"status": status, "student_id": student_id, "first_name": first_name, "group": group,
             "start_expire_date": start_expire_date,
             "end_expire_date": end_expire_date})
        return context

    def get_csv_info(self, user):
        return [
            user.userprofile.get_sn(),
            user.username,
            user.first_name,
            user.userprofile.preuser.get_gender(),
            user.userprofile.preuser.mobile,
            user.userprofile.preuser.wx,
            user.userprofile.preuser.birthday,
            user.userprofile.preuser.get_source(),
            user.userprofile.preuser.province,
            user.userprofile.preuser.city,

        ]

    def get_csv_headers(self):
        return [
            '序号'.encode('utf-8'),
            '缦客号'.encode('utf-8'),
            '用户名'.encode('utf-8'),
            '姓名'.encode('utf-8'),
            '性别'.encode('utf-8'),
            '电话'.encode('utf-8'),
            '微信'.encode('utf-8'),
            '出生日期'.encode('utf-8'),
            '来源'.encode('utf-8'),
            '省'.encode('utf-8'),
            '市'.encode('utf-8'),

        ]

    def get(self, request, *args, **kwargs):
        self.queryset = self.search()
        if request.GET.get("export"):
            rows = ([(i + 1).__str__()] + self.get_csv_info(user) for i, user in enumerate(self.queryset))
            return export_csv('用户信息'.encode('utf-8'), self.get_csv_headers(), rows)
        else:
            return super(UserList, self).get(request, *args, **kwargs)


@method_decorator(cls_decorator(cls_name='UserDetail'), name='dispatch')
class UserDetail(DetailView):
    model = User
    template_name = 'bee_django_user/user/detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        if "cc" in settings.COURSE_LIVE_PROVIDER_LIST:
            context["cc"] = True
        if "gensee" in settings.COURSE_LIVE_PROVIDER_LIST:
            context["gensee"] = True
        return context


class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('bee_django_user:user_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


# @method_decorator(cls_decorator(cls_name='UserCreate'), name='dispatch')
# class UserCreate(TemplateView):
#     # model = User
#     # form_class = UserCreateForm
#     template_name = 'bee_django_user/user/create.html'
#     # success_url = reverse_lazy('bee_django_user:user_list')
#
#     # def get_context_data(self, **kwargs):
#     #     context = super(UserCreate, self).get_context_data(**kwargs)
#     #     context["preuser"] = PreUser.objects.get(id=self.kwargs["preuser_id"])
#     #     return context
#
#     @transaction.atomic
#     def _create_user(self, preuser, preuser_fee_id):
#         try:
#             # 学号
#             max_student_id = UserProfile.get_max_student_id()
#             user_profile = UserProfile()
#             user_profile.preuser = preuser
#             user_profile.student_id = max_student_id + 1
#             # sn
#             max_sn = UserProfile.get_max_sn()
#             sn = UserSN.get_next_sn(max_sn)
#             if not sn:
#                 messages.error(self.request, '统一缦客号生成错误')
#                 return
#             user_profile.sn = sn
#             user_profile.save()
#             # user_profile.create_user(preuser_fee_id)
#             user = user_profile.user
#             # res, msg = after_check_callback(preuser_fee_id, user=user, new_user=True)
#             messages.success(self.request, '添加用户成功')
#         except Exception as e:
#             print(e)
#             messages.error(self.request, '发生错误')
#
#     @transaction.atomic
#     def get(self, request, *args, **kwargs):
#         # print(self.kwargs)
#         preuser_id = request.GET["preuser_id"]
#         preuser_fee_id = request.GET["preuser_fee_id"]
#         if not self.request.user.has_perm('bee_django_user.add_userprofile'):
#             messages.error(self.request, '没有权限')
#             return redirect(reverse('bee_django_crm:preuser_fee_detail', kwargs={"pk": preuser_fee_id}))
#         # preuser = PreUser.objects.get(id=preuser_id)
#         try:
#             user_profile = preuser.userprofile
#             user = user_profile.user
#             if preuser_fee_id:
#                 res, msg = after_check_callback(preuser_fee_id, user=user, new_user=False)
#                 messages.success(self.request, '已添加过用户，后续操作成功')
#             else:
#                 messages.success(self.request, '已添加过用户')
#         except UserProfile.DoesNotExist:
#             self._create_user(preuser, preuser_fee_id)
#         except:
#             messages.success(self.request, '发生错误')
#
#         if preuser.level == 3:
#             return redirect(reverse('bee_django_crm:preuser_fee_list', kwargs={'preuser_id': 0}))
#         elif preuser.level == 4:
#             return redirect(reverse('bee_django_crm:preuser_list') + "?level=4")
#
#         return

# class CodeUserCreate(TemplateView):
#     template_name = 'bee_django_user/user/create.html'
#
#     @transaction.atomic
#     def get(self, request, *args, **kwargs):
#         # print(self.kwargs)
#         preuser_id = request.GET["preuser_id"]
#         if not self.request.user.has_perm('bee_django_user.add_userprofile'):
#             messages.error(self.request, '没有权限')
#             return redirect(reverse('bee_django_crm:preuser_list') + "?level=4")
#         preuser = PreUser.objects.get(id=preuser_id)
#         try:
#             user_profile = preuser.userprofile
#             user = user_profile.user
#             messages.error(self.request, '已创建过账号')
#             return redirect(reverse('bee_django_user:detail', kwargs={'pk': user.id}))
#         except UserProfile.DoesNotExist:
#             try:
#                 # student_id
#                 max_student_id = get_max_student_id()
#                 user_profile = UserProfile()
#                 user_profile.preuser = preuser
#                 user_profile.student_id = max_student_id + 1
#                 # sn
#                 max_sn = get_max_sn()
#                 sn = UserSN.get_next_sn(max_sn)
#                 if not sn:
#                     messages.error(self.request, '统一缦客号生成错误')
#                     return redirect(reverse('bee_django_crm:preuser_list') + "?level=4")
#                 user_profile.sn = sn
#                 user_profile.save()
#                 user = user_profile.user
#                 messages.success(self.request, '添加用户成功')
#             except Exception as e:
#                 print(e)
#                 messages.error(self.request, '发生错误')
#
#         return redirect(reverse('bee_django_crm:preuser_list') + "?level=4")


@method_decorator(cls_decorator(cls_name='UserUpdate'), name='dispatch')
# @method_decorator(permission_required("change_user"), name='dispatch')
class UserUpdate(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'bee_django_user/user/form.html'

    def get_success_url(self):
        return reverse_lazy("bee_django_user:user_detail", kwargs=self.kwargs)

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        context["formset"] = profile_inline_formset(instance=self.object)
        return context

    @transaction.atomic
    def form_valid(self, form):
        if not self.request.user.has_perm('bee_django_user.change_userprofile'):
            messages.error(self.request, '没有权限')
            return redirect(reverse('bee_django_user:user_update', kwargs=self.kwargs))
        formset = profile_inline_formset(self.request.POST, self.request.FILES, instance=self.object)
        if formset.is_valid():
            # profile = formset.cleaned_data[0]

            # profile.agent=agent
            # print(agent)
            # agent = profile['agent']
            # print(agent)
            self.object.userprofile.save()
            messages.success(self.request, '修改成功')
        return super(UserUpdate, self).form_valid(form)


@method_decorator(cls_decorator(cls_name='UserUpdate'), name='dispatch')
class UserGroupUpdate(UpdateView):
    model = User
    form_class = UserGroupForm
    template_name = 'bee_django_user/group/user_group_form.html'

    def get_success_url(self):
        return reverse_lazy("bee_django_user:user_detail", kwargs=self.kwargs)


class UserSNUpdate(UpdateView):
    model = UserProfile
    form_class = UserSNForm
    template_name = 'bee_django_user/user/user_sn_form.html'

    def get_success_url(self):
        user_profile_id = self.kwargs['pk']
        user = User.objects.get(userprofile__id=user_profile_id)
        return reverse_lazy("bee_django_user:user_detail", kwargs={"pk": user.id})

    def get_context_data(self, **kwargs):
        context = super(UserSNUpdate, self).get_context_data(**kwargs)
        context["sn_list"] = UserSN.objects.all()
        user_profile_id = self.kwargs['pk']
        user = User.objects.get(userprofile__id=user_profile_id)
        context["user"] = user
        context["max_sn"] = UserProfile.get_max_sn()
        return context


@method_decorator(permission_required('bee_django_user.add_userclassremoverecord'), name='dispatch')
class UserClassUpdate(UpdateView):
    model = UserProfile
    form_class = UserProfileUpdateClassForm
    template_name = 'bee_django_user/user/user_class_form.html'

    def get_success_url(self):
        user_profile_id = self.kwargs['pk']
        user = User.objects.get(userprofile__id=user_profile_id)
        return reverse_lazy("bee_django_user:user_detail", kwargs={"pk": user.id})

    def get_context_data(self, **kwargs):
        context = super(UserClassUpdate, self).get_context_data(**kwargs)
        return context

    @transaction.atomic
    def form_valid(self, form):
        user_profile_id = self.kwargs['pk']
        user_profile = UserProfile.objects.get(id=user_profile_id)
        old_class = user_profile.user_class
        new_class = form.instance.user_class
        if not old_class == new_class:
            UserClassRemoveRecord(student=user_profile.user, old_class=old_class, new_class=new_class,
                                  created_by=self.request.user).save()

        return super(UserClassUpdate, self).form_valid(form)


class UserParentUpdateTemplate(TemplateView):
    template_name = 'bee_django_user/user/user_parent.html'

    def get_context_data(self, **kwargs):
        context = super(UserParentUpdateTemplate, self).get_context_data(**kwargs)
        user_id = self.kwargs['student_id']
        user = User.objects.get(id=user_id)
        context["user"] = user
        context["user_parent_relation"] = UserProfileParentRelation.objects.filter(student=user.userprofile)
        context["form"] = UserProfileParentsForm()
        return context

    def get(self, request, *args, **kwargs):
        return super(UserParentUpdateTemplate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs['student_id']
        user = User.objects.get(id=user_id)
        form = UserProfileParentsForm(request.POST)
        if form.is_valid():
            parent = form.cleaned_data['parent']
            UserProfileParentRelation.objects.create(student=user.userprofile, parent=parent.userprofile)
            messages.success(request, '添加成功')
            # user.userprofile.parents.add(parent)
        else:
            messages.error(request, '填写错误')
        return redirect(reverse_lazy('bee_django_user:user_parent_update', kwargs=self.kwargs))


class UserParentDelete(DeleteView):
    model = UserProfileParentRelation
    success_url = reverse_lazy('bee_django_user:user_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


class UserPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('bee_django_user:user_password_change_done')
    template_name = 'bee_django_user/user/password_change.html'


class UserPasswordResetView(TemplateView):
    template_name = 'bee_django_user/user/password_reset.html'

    def get(self, request, *args, **kwargs):
        return super(UserPasswordResetView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user_id = self.kwargs['pk']
        user = User.objects.get(id=user_id)
        form = AdminPasswordChangeForm(user)
        context = super(UserPasswordResetView, self).get_context_data(**kwargs)
        context["form"] = form
        context["user"] = user
        return context

    def post(self, request, *args, **kwargs):
        user_id = self.kwargs['pk']
        user = User.objects.get(id=user_id)
        form = AdminPasswordChangeForm(user, request.POST)
        if form.is_valid():
            if request.user.has_perm("bee_django_user.reset_user_password"):
                form.save()
                messages.success(request, '密码已经更新!')
            else:
                messages.error(request, '没有权限')
        else:
            messages.error(request, '请修正以下错误')
        return redirect(reverse_lazy('bee_django_user:user_password_reset', kwargs={'pk': user_id}))


# 用户组权限
@method_decorator(cls_decorator(cls_name='GroupList'), name='dispatch')
class GroupList(ListView):
    model = Group
    template_name = 'bee_django_user/group/list.html'
    context_object_name = 'group_list'
    paginate_by = 20


# 请假，禁用 状态

class StatusSave(TemplateView):
    def post(self, request, *args, **kwargs):
        is_pause = request.POST.get("is_pause")
        is_disable = request.POST.get("is_disable")
        user_id = request.POST.get("user_id")
        user = User.objects.get(id=user_id)
        is_pause = True if is_pause == "1" else False
        is_disable = True if is_disable == "1" else False
        is_active = not is_disable
        user.is_active = is_active
        user.userprofile.is_pause = is_pause
        user.save()
        user.userprofile.save()
        # 发送信号
        _info = '【' + self.request.user.first_name + "】于【" + localtime().strftime(
            "%Y-%m-%d %H:%M:%S") + "】操作"
        update_user_active_pause_signal.send(sender=UserProfile, user=user, active=is_active, pause=is_pause,
                                             info=_info)
        return JsonResponse(data={
            'error': 0,
            'message': '修改成功'
        })


class AvatarUpdate(UpdateView):
    model = UserProfile
    form_class = UserAvatarForm
    template_name = 'bee_django_user/user/avatar_form.html'

    def get_success_url(self):
        user = self._get_user()
        return reverse_lazy('bee_django_user:user_detail', kwargs={"pk": user.id})

    def _get_user(self):
        userprofle = UserProfile.objects.get(id=self.kwargs["pk"])
        return userprofle.user

    def get_context_data(self, **kwargs):
        context = super(AvatarUpdate, self).get_context_data(**kwargs)
        context["user"] = self._get_user()
        return context

    @transaction.atomic
    def form_valid(self, form):
        rc = super(AvatarUpdate, self).form_valid(form)

        img = Image.open(form.instance.avatar)

        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    exif = dict(img._getexif().items())

                    if exif[orientation] == 3:
                        img = img.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        img = img.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        img = img.rotate(90, expand=True)

                    break
        except:
            pass

        thumbnail = img.resize((100, 100), Image.ANTIALIAS)
        thumbnail = thumbnail.crop((0, 0, 100, 100))
        thumbnail.save(form.instance.avatar.path)

        img.close()
        return rc


class RoomSave(TemplateView):
    def save_cc_room(self, userprofile, _type):
        try:
            from bee_django_course.cc import create_room
            if _type == 'create':
                room = create_room(userprofile.user.first_name + "的直播间")
                if room:
                    userprofile.room_id = room
                    userprofile.save()
                    return True
                return False
            elif _type == 'delete':
                return False
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def save_gensee_room(self, userprofile, _type):
        try:
            from bee_django_course.gensee import create_room, delete_room
            if _type == 'create':
                room = create_room(userprofile.user.first_name + "的直播间")
                if room:
                    userprofile.gensee_room_id = room
                    userprofile.save()
                    return True
                return False
            elif _type == 'delete':
                res = delete_room(userprofile.gensee_room_id)
                if res == True:
                    userprofile.gensee_room_id = None
                    userprofile.save()
                return res
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def post(self, request, *args, **kwargs):
        user_id = request.POST.get("user_id")
        provider_name = request.POST.get("provider")
        _type = request.POST.get("t")
        userprofile = UserProfile.objects.get(user_id=user_id)
        cc_res = False
        gensee_res = False
        if provider_name == 'cc':
            cc_res = self.save_cc_room(userprofile, _type)
        if provider_name == 'gensee':
            gensee_res = self.save_gensee_room(userprofile, _type)
        return JsonResponse(data={
            'cc_res': cc_res,
            "gensee_res": gensee_res
        })


# 请假记录
class LeaveList(ListView):
    model = UserLeaveRecord
    template_name = 'bee_django_user/leave/list.html'
    queryset = None
    context_object_name = 'record_list'
    paginate_by = 20

    def get_user(self):
        return User.objects.get(id=self.kwargs["user_id"])

    def get_queryset(self):
        user = self.get_user()
        return UserLeaveRecord.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super(LeaveList, self).get_context_data(**kwargs)
        context["user"] = self.get_user()
        return context


class LeaveDetail(DetailView):
    model = UserLeaveRecord
    template_name = 'bee_django_user/leave/detail.html'
    context_object_name = 'record'


# 添加请假记录
class LeaveCreate(CreateView):
    model = UserLeaveRecord
    form_class = UserLeaveRecordForm
    template_name = 'bee_django_user/leave/form.html'
    success_url = None

    def get_success_url(self):
        return reverse_lazy('bee_django_user:leave_list', kwargs=self.kwargs)

    def get_user(self):
        return User.objects.get(id=self.kwargs["user_id"])

    def get_context_data(self, **kwargs):
        context = super(LeaveCreate, self).get_context_data(**kwargs)

        context["user"] = self.get_user()
        return context

    def form_valid(self, form):
        days = None
        user = self.get_user()
        user_profile = user.userprofile
        form.instance.user = user
        if form.instance.end and form.instance.start:
            days = form.instance.end - form.instance.start
        form.instance.old_expire = user_profile.expire_date
        form.instance.created_by = self.request.user

        _info = ''
        # 请假
        if form.instance.type in [1]:
            if not days or days.days < 0:
                messages.error(self.request, '开始日期或结束日期填写错误')
                return redirect(reverse_lazy('bee_django_user:leave_add', kwargs=self.kwargs))
            if user_profile.expire_date:
                form.instance.new_expire = (user_profile.expire_date + datetime.timedelta(days=days.days))
            else:
                messages.error(self.request, '请先填写该学生结课日期，或选择【延期/提前】类型')
                return redirect(reverse_lazy('bee_django_user:leave_add', kwargs=self.kwargs))
            _info = '请假'
        # if form.instance.type in [2]:
        #     if user_profile.expire_date:
        #         form.instance.new_expire = (user_profile.expire_date - datetime.timedelta(days=days.days))
        # 延期/提前
        if form.instance.type in [3]:
            _info = '延期'
            form.instance.new_expire = form.instance.end
        if form.instance.type in [4]:
            _info = '提前'
            form.instance.new_expire = form.instance.end

        # 详情
        info = '<p>=====以下由【' + self.request.user.first_name + '】于【' + datetime.datetime.now(
            tz=LOCAL_TIMEZONE).strftime("%Y-%m-%d %H:%M") + '】添加' + _info + '=====</p>'
        info += "<p>" + _info + "开始日期：" + localtime(form.instance.start).strftime("%Y-%m-%d %H:%M")
        info += "<p>" + _info + "结束日期：" + localtime(form.instance.end).strftime("%Y-%m-%d %H:%M")
        info += "<p>原结课日期：" + localtime(user.userprofile.expire_date).strftime("%Y-%m-%d %H:%M")
        info += "<p>新结课日期：" + localtime(form.instance.new_expire).strftime("%Y-%m-%d %H:%M")
        info += "<p>" + form.instance.info + "</p>"
        form.instance.info = info
        return super(LeaveCreate, self).form_valid(form)


# 审核请假
class LeaveUpdateCheck(TemplateView):
    def post(self, request, *args, **kwargs):
        record_id = self.request.POST.get('record_id')
        if not request.user.has_perm("bee_django_user.change_check"):
            return JsonResponse(data={
                'error': 1,
                'message': '没有权限'
            })
        record = UserLeaveRecord.objects.get(id=record_id)
        if record.is_check == True:
            return JsonResponse(data={
                'error': 1,
                'message': '已审核过'
            })
        record.is_check = True
        record.check_at = datetime.datetime.now()
        record.check_by = self.request.user
        record.save()

        return JsonResponse(data={
            'error': 0,
            'message': '审核成功'
        })


# 销假
class LeaveCancel(TemplateView):
    model = UserLeaveRecord
    template_name = 'bee_django_user/leave/form_cancel.html'

    def get_record(self):
        record = UserLeaveRecord.objects.get(id=self.kwargs["pk"])
        return record

    def get_context_data(self, **kwargs):
        context = super(LeaveCancel, self).get_context_data(**kwargs)
        record = UserLeaveRecord.objects.get(id=self.kwargs["pk"])
        context["record"] = record
        context["form"] = UserLeaveRecordCancelForm()
        context["temp_end_start"] = record.end - datetime.timedelta(days=1)
        return context

    def post(self, request, *args, **kwargs):
        form = UserLeaveRecordCancelForm(request.POST)
        if form.is_valid():
            record = self.get_record()
            user = record.user
            user_profile = user.userprofile
            s_days = form.instance.start - record.start
            e_days = record.end - form.instance.start

            if s_days.days < 0 or e_days.days <= 0:
                messages.error(request, '开始日期填写错误')
                return redirect(reverse_lazy('bee_django_user:leave_cancel', kwargs=self.kwargs))
            if not user_profile.expire_date:
                messages.error(request, '请先填写该学生结课日期，或选择【延期/提前】类型')
                return redirect(reverse_lazy('bee_django_user:leave_add', kwargs={"user_id": user.id}))
            record.new_expire = (user_profile.expire_date - datetime.timedelta(days=e_days.days))
            record.type = 2
            record.end = form.instance.start
            info = record.info + '<p>=====以下由【' + request.user.first_name + '】于【' + datetime.datetime.now(
                tz=LOCAL_TIMEZONE).strftime("%Y-%m-%d %H:%M") + '】添加销假=====</p>'
            info += "<p>结束休假日期：" + form.instance.start.strftime("%Y-%m-%d")
            info += "<p>原结课日期：" + localtime(user.userprofile.expire_date).strftime("%Y-%m-%d %H:%M")
            info += "<p>新结课日期：" + localtime(record.new_expire).strftime("%Y-%m-%d %H:%M")
            info += "<p>" + form.instance.info + "</p>"
            record.info = info
            record.save()
            return redirect(reverse_lazy('bee_django_user:leave_list', kwargs={"user_id": user.id}))
        else:
            messages.error(request, '出错了')
            return redirect(reverse_lazy('bee_django_user:leave_cancel', kwargs=self.kwargs))
            # return super(LeaveCancel, self).form_valid(form)


class LeaveDelete(DeleteView):
    model = UserLeaveRecord
    success_url = None

    def get_success_url(self):
        record = UserLeaveRecord.objects.get(id=self.kwargs["pk"])
        return reverse_lazy('bee_django_user:leave_list', kwargs={"user_id": record.user.id})

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


# ========class 班级===========
@method_decorator(cls_decorator(cls_name='ClassList'), name='dispatch')
class ClassList(ListView):
    model = UserClass
    template_name = 'bee_django_user/class/list.html'
    context_object_name = 'class_list'
    paginate_by = 20

    def _get_class_name(self):
        class_id = self.request.GET.get("class_id")
        class_name = self.request.GET.get("class_name")
        if not class_name in [0, "0", None]:
            return class_name
        if not class_id in [0, "0", None]:
            return UserClass.objects.get(id=class_id).name

    def _get_mentor_name(self):
        mentor_id = self.request.GET.get("mentor_id")
        assistant_name = self.request.GET.get("assistant_name")
        if not assistant_name in [0, "0", None]:
            return assistant_name
        if not mentor_id in [0, "0", None]:
            return User.objects.get(id=mentor_id).first_name

    def search(self):
        # if self.request.user.has_perm("bee_django_user.view_all_classes"):
        #     queryset = UserClass.objects.all()
        # elif self.request.user.has_perm("bee_django_user.view_teach_classes"):
        #     queryset = UserClass.objects.filter(assistant=self.request.user)
        # else:
        #     return UserClass.objects.none()
        queryset = self.request.user.userprofile.get_class_list()
        status = self.request.GET.get("status")
        class_id = self.request.GET.get("class_id")
        class_name = self._get_class_name()
        mentor_id = self.request.GET.get("mentor_id")
        assistant_name = self._get_mentor_name()
        lecturer_name = self.request.GET.get("lecturer_name")
        agent_name = self.request.GET.get("agent_name")

        if not status in [0, "0", None, '']:
            queryset = queryset.filter(status=status)
        if not class_id in [0, "0", None, '']:
            queryset = queryset.filter(id=class_id)

        if not class_name in [0, "0", None, '']:
            queryset = queryset.filter(name__icontains=class_name)

        # 助教
        if not mentor_id in [0, "0", None, '']:
            queryset = queryset.filter(assistant_id=mentor_id)
        if assistant_name:
            try:
                kwargs = {}  # 动态查询的字段
                name_field = settings.USER_NAME_FIELD
                if assistant_name == '无':
                    kwargs["assistant__" + name_field + '__isnull'] = True
                else:
                    kwargs["assistant__" + name_field + '__icontains'] = assistant_name
                queryset = queryset.filter(**kwargs)
            except:
                pass

        if lecturer_name:
            try:
                kwargs = {}  # 动态查询的字段
                name_field = settings.USER_NAME_FIELD
                if lecturer_name == '无':
                    kwargs["lecturer__" + name_field + '__isnull'] = True
                else:
                    kwargs["lecturer__" + name_field + '__icontains'] = lecturer_name
                queryset = queryset.filter(**kwargs)
            except:
                pass

        if agent_name:
            try:
                kwargs = {}  # 动态查询的字段
                name_field = settings.USER_NAME_FIELD
                if agent_name == '无':
                    kwargs["agent__" + name_field + '__isnull'] = True
                else:
                    kwargs["agent__" + name_field + '__icontains'] = agent_name
                queryset = queryset.filter(**kwargs)
            except:
                pass

        return queryset

    def get_queryset(self):
        return self.search()

    def get_context_data(self, **kwargs):
        context = super(ClassList, self).get_context_data(**kwargs)
        status = self.request.GET.get("status")
        class_name = self._get_class_name()
        assistant_name = self._get_mentor_name()
        lecturer_name = self.request.GET.get("lecturer_name")
        agent_name = self.request.GET.get("agent_name")

        context['search_form'] = UserClassSearchForm(
            {"status": status, "class_name": class_name, "assistant_name": assistant_name,
             "lecturer_name": lecturer_name, "agent_name": agent_name})
        return context


class ClassDashboard(ClassList):
    template_name = 'bee_django_user/class/dashboard.html'
    paginate_by = 1

    # def get_queryset(self):
    #     user_class_id = self.request.GET.get("class_id")
    #     if not user_class_id in [0,"0",None]:
    #         return UserClass.objects.filter(id=user_class_id)
    #     return

    def get_context_data(self, **kwargs):
        context = super(ClassDashboard, self).get_context_data(**kwargs)
        status = self.request.GET.get("status")
        class_name = self._get_class_name()
        time = self.request.GET.get("time")  # 时间段
        context['search_form'] = UserClassDashBoardSearchForm(
            {"status": status, "class_name": class_name, "time": time})
        context["time"] = time
        return context


@method_decorator(cls_decorator(cls_name='ClassDetail'), name='dispatch')
class ClassDetail(DetailView):
    model = UserClass
    template_name = 'bee_django_user/class/detail.html'
    context_object_name = 'class'

    # def get_context_data(self, **kwargs):
    #     context=super(ClassDetail,self).get_context_data(kwargs)
    #     context["students"]=None
    #     return context


@method_decorator(cls_decorator(cls_name='ClassCreate'), name='dispatch')
class ClassCreate(CreateView):
    model = UserClass
    form_class = UserClassForm
    template_name = 'bee_django_user/class/form.html'
    success_url = reverse_lazy('bee_django_user:class_list')

    def get_form_kwargs(self):
        kwargs = super(ClassCreate, self).get_form_kwargs()
        kwargs.update({
            'request_user': self.request.user
        })
        return kwargs


@method_decorator(cls_decorator(cls_name='ClassUpdate'), name='dispatch')
class ClassUpdate(UpdateView):
    model = UserClass
    form_class = UserClassForm
    template_name = 'bee_django_user/class/form.html'

    def get_form_kwargs(self):
        kwargs = super(ClassUpdate, self).get_form_kwargs()
        kwargs.update({
            'request_user': self.request.user
        })
        return kwargs

    @transaction.atomic
    def form_valid(self, form):
        if not self.request.user.has_perm('bee_django_user.change_userclass'):
            messages.error(self.request, '没有权限')
            return redirect(reverse('bee_django_user:class_update', kwargs=self.kwargs))
        return super(ClassUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bee_django_user:class_detail', kwargs=self.kwargs)


# ==== 用户升级======
class LevelList(ListView):
    model = UserLevel
    template_name = 'bee_django_user/level/level_list.html'
    context_object_name = 'level_list'
    paginate_by = 20


class LevelDetail(DetailView):
    model = UserLevel
    template_name = 'bee_django_user/level/level_detail.html'
    context_object_name = 'level'


class LevelCreate(CreateView):
    model = UserLevel
    form_class = UserLevelCreateForm
    template_name = 'bee_django_user/level/level_form.html'


class LevelUpdate(UpdateView):
    model = UserLevel
    form_class = UserLevelUpdateForm
    template_name = 'bee_django_user/level/level_form.html'

    # def get_context_data(self, **kwargs):
    #     context = super(GradeUpdate, self).get_context_data(**kwargs)
    #     grade_id = self.kwargs["pk"]
    #     grade = Grade.objects.get(id=grade_id)
    #     context["cert"] = grade.cert_image
    #     return context


class LevelDelete(DeleteView):
    model = UserLevel
    success_url = reverse_lazy('bee_django_user:level_list')

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)


class LevelRecrodList(ListView):
    model = UserLevelUpRecord
    template_name = 'bee_django_user/level/record_list.html'
    paginate_by = 20
    context_object_name = 'record_list'
    queryset = None

    def get(self, request, *args, **kwargs):
        if not self.kwargs.has_key("user_id"):
            self.kwargs["user_id"] = 0
        return super(LevelRecrodList, self).get(request)

    def get_user(self):
        user_id = self.kwargs["user_id"]
        if not user_id in [None, '0', 0]:
            user = User.objects.get(id=user_id)
        else:
            user = None
        return user

    def search(self):
        name = self.request.GET.get("name")
        title = self.request.GET.get("title")
        status = self.request.GET.get("status")
        user = self.get_user()

        if self.request.user.has_perm("bee_django_user.view_all_level_up_records"):
            self.queryset = UserLevelUpRecord.objects.all()
        else:
            user_collection = self.request.user.get_student_list()
            self.queryset = UserLevelUpRecord.objects.filter(user__in=user_collection)
        if user:
            self.queryset = self.queryset.filter(user=user)

        if not title in ["", 0, None]:
            self.queryset = self.queryset.filter(level__title=title)
        if not status in ["", '0', 0, None]:
            self.queryset = self.queryset.filter(status=status)
        if not name in ["", 0, None]:
            self.queryset = self.queryset.filter(user__first_name__icontains=name)
        return self.queryset

    def get_queryset(self):
        return self.search()

    def get_context_data(self, **kwargs):
        context = super(LevelRecrodList, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        title = self.request.GET.get("title")
        status = self.request.GET.get("status")
        context['search_form'] = UserLevelUpRecordSearchForm(
            {"name": name, "title": title, "status": status})
        context["user"] = self.get_user()
        return context


class LevelRecrodDetail(DetailView):
    model = UserLevelUpRecord
    template_name = 'bee_django_user/level/record_detail.html'
    context_object_name = 'record'


class LevelRecrodCreate(CreateView):
    model = UserLevelUpRecord
    form_class = UserLevelUpRecordCreateForm
    template_name = 'bee_django_user/level/record_form.html'

    def get_context_data(self, **kwargs):
        context = super(LevelRecrodCreate, self).get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs["user_id"])
        context["record"] = {"user": user}
        return context

    @transaction.atomic
    def form_valid(self, form):
        user = User.objects.get(id=self.kwargs["user_id"])
        level = form.instance.level
        res, msg = UserLevelUpRecord.check_add_user_record(user, level)
        if res == False:
            messages.error(self.request, msg)
            return redirect(reverse("bee_django_user:level_record_add", kwargs=self.kwargs))
        form.instance.user = user
        record = form.save(commit=False)
        record.chenge_status(self.request.user, "create")
        return super(LevelRecrodCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse("bee_django_user:level_record_list", kwargs=self.kwargs)


class LevelRecrodUpdate(UpdateView):
    model = UserLevelUpRecord
    form_class = UserLevelUpRecordUpdateForm
    template_name = 'bee_django_user/level/record_form.html'

    def get_context_data(self, **kwargs):
        context = super(LevelRecrodUpdate, self).get_context_data(**kwargs)
        record = UserLevelUpRecord.objects.get(id=self.kwargs["pk"])
        context["record"] = record
        return context

    @transaction.atomic
    def form_valid(self, form):
        status = form.cleaned_data['status']
        result = form.cleaned_data['result']
        if status == -1:
            s = 'open'
        elif status == -2:
            s = 'apply'
        elif status == 1:
            s = 'pass'
        elif status == 2:
            s = 'reject'
        elif status == 3:
            s = 'close'
        else:
            s = ''
        record = form.save(commit=False)
        record.chenge_status(op_user=self.request.user, _type=s, result=result)
        return super(LevelRecrodUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse("bee_django_user:level_record_detail", kwargs=self.kwargs)


class CustomLevelRecrodList(LevelRecrodList):
    template_name = 'bee_django_user/level/custom_record_list.html'


class CustomLevelRecrodApply(LevelRecrodUpdate):
    model = UserLevelUpRecord
    form_class = CustomUserLevelUpRecordApplyForm
    template_name = 'bee_django_user/level/custom_record_form.html'

    @transaction.atomic
    def form_valid(self, form):
        record = form.save(commit=False)
        try:
            record.application = form.cleaned_data['application']
        except:
            pass
        try:
            record.supplement = form.cleaned_data['supplement']
        except:
            pass
        if not record.user == self.request.user:
            messages.error(self.request, '申请人错误')
            return redirect(reverse("bee_django_user:custom_level_record_apply", kwargs=self.kwargs))
        if record.can_apply():
            messages.success(self.request, '提交成功，请等待审核结果')
            record.chenge_status(op_user=self.request.user, _type='apply')
        elif record.can_supply():
            messages.success(self.request, '提交成功')
            record.chenge_status(op_user=self.request.user, _type='supply')
        else:
            messages.error(self.request, '当前不可提交内容，请等待下一步处理')
        return super(LevelRecrodUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse("bee_django_user:custom_level_record_list", kwargs={"user_id": self.request.user.id})


@method_decorator(permission_required('bee_django_user.can_edit_permission'), name='dispatch')
class UserPermisionList(ListView):
    model = CustomAuthPermission
    template_name = 'bee_django_user/user/permission.html'
    paginate_by = 20
    context_object_name = 'permission_list'

    def get_queryset(self):
        name = self.request.GET.get("name")
        q = CustomAuthPermission.objects.all()
        if not name in ['', None]:
            q = q.filter(
                Q(app_title__icontains=name) | Q(model_title__icontains=name) | Q(codename_title__icontains=name))
        return q

    def get_context_data(self, **kwargs):
        context = super(UserPermisionList, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        all_group_list = Group.objects.all()
        group_list = []
        for group in all_group_list:
            if group.permissions.filter(codename='can_manage').exists():
                group_list.append(group)
        context["group_list"] = group_list
        context[
            "tips_group"] = UserProfile.get_assistant_groupname_list() + UserProfile.get_lecturer_groupname_list() + UserProfile.get_agent_groupname_list()
        context["search_form"] = PermissionSearchForm(data={"name": name})
        return context

    # def get(self, request, *args, **kwargs):
    #     group_list = Group.objects.all()


@method_decorator(permission_required('bee_django_user.can_edit_permission'), name='dispatch')
class UserPermisionUpdate(TemplateView):
    # model = CustomAuthPermission
    # form_class = UserPermisionUpdateForm
    template_name = 'bee_django_user/user/permission_form.html'

    def get_context_data(self, **kwargs):
        context = super(UserPermisionUpdate, self).get_context_data(**kwargs)
        group = Group.objects.get(id=self.kwargs["group_id"])
        custom_permission = CustomAuthPermission.objects.get(id=self.kwargs["pk"])
        context["group"] = group
        context["custom_permission"] = custom_permission
        has_permission = False
        if group.permissions.filter(codename=custom_permission.auth_permission.codename).exists():
            has_permission = True
        context["form"] = UserPermisionUpdateForm(data={"has_permission": has_permission})
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = UserPermisionUpdateForm(data=request.POST)
        if form.is_valid():
            group = Group.objects.get(id=self.kwargs["group_id"])
            custom_permission = CustomAuthPermission.objects.get(id=self.kwargs["pk"])
            has_permission = form.cleaned_data["has_permission"]
            permission = custom_permission.auth_permission
            if has_permission:
                group.permissions.add(permission)
            else:
                group.permissions.remove(permission)
        else:
            messages.error(request, '错误')
        return redirect(reverse("bee_django_user:user_permission"))


class UserPermisionResetTemplate(TemplateView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return JsonResponse(data={
                'error': 1,
                'message': '没有权限'
            })
        group_id = self.request.POST.get("group_id")
        group = Group.objects.get(id=group_id)
        permissions = CustomAuthPermission.objects.filter(can_edit=True)
        for p in permissions:
            permission = p.auth_permission
            group.permissions.add(permission)
        return JsonResponse(data={
            'error': 0,
            'message': '成功'
        })


class WxServiceUserBind(TemplateView):
    template_name = 'bee_django_user/user/wx_bind.html'
    openid = None

    def get_context_data(self, **kwargs):
        context = super(WxServiceUserBind, self).get_context_data(**kwargs)
        context["form"] = UserProfileWxServicBindForm()
        # self.openid=self.request.GET.get("openid")
        # print self.request.GET.get("openid")
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = UserProfileWxServicBindForm(data=request.POST)
        openid = self.request.GET.get("openid")
        if form.is_valid():
            # openid = self.request.POST.get("openid")
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = auth.authenticate(username=username, password=password)
            if user is None or not user.is_active:
                messages.error(self.request, '用户名或密码错误')
                return redirect(reverse("bee_django_user:wx_service_user_bind") + "?openid=" + openid)
            if user.userprofile.wxservice_openid:
                messages.error(self.request, '该用户已绑定过微信')
                return redirect(reverse("bee_django_user:wx_service_user_bind") + "?openid=" + openid)
            if openid in ["", None]:
                messages.error(self.request, '参数错误')
                return redirect(reverse("bee_django_user:wx_service_user_bind") + "?openid=" + openid)
            _list = UserProfile.objects.filter(wxservice_openid=openid)
            if _list.exists():
                messages.error(self.request, '该微信已绑定过用户')
                return redirect(reverse("bee_django_user:wx_service_user_bind") + "?openid=" + openid)
            user.userprofile.wxservice_openid = openid
            user.userprofile.save()
            messages.success(self.request, '绑定成功')
            return redirect(reverse("bee_django_user:wx_service_user_bind") + "?openid=" + openid)
        else:
            messages.error(self.request, '填写错误')
            return redirect(reverse("bee_django_user:wx_service_user_bind") + "?openid=" + openid)
