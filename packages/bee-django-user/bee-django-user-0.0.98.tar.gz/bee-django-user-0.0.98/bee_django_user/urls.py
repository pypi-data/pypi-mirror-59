#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bee'
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views, wxapp

app_name = "bee_django_user"

urlpatterns = [
    url(r'^test/$', views.test, name='test'),
    url(r'^$', views.UserList.as_view(), name='index'),

    url(r'^login/$', auth_views.LoginView.as_view(template_name='bee_django_user/user/login.html'), name='user_login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/user/login'}, name='user_logout'),
    url(r'^password/change/$', views.UserPasswordChangeView.as_view(), name='user_password_change'),
    url(r'^password/change/done/$', auth_views.PasswordChangeDoneView.as_view(
        template_name='bee_django_user/user/password_change_done.html'
    ), name='user_password_change_done'),
    url(r'^password/reset/(?P<pk>[0-9]+)/$', views.UserPasswordResetView.as_view(), name='user_password_reset'),

    # 学生
    url(r'^list/$', views.UserList.as_view(), name='user_list'),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user_detail'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.UserDelete.as_view(), name='user_delete'),
    # url(r'^create/$', views.UserCreate.as_view(), name='user_create'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.UserUpdate.as_view(), name='user_update'),
    url(r'^group/update/(?P<pk>[0-9]+)/$', views.UserGroupUpdate.as_view(), name='user_group_update'),
    url(r'^sn/update/(?P<pk>[0-9]+)/$', views.UserSNUpdate.as_view(), name='user_sn_update'),
    url(r'^userclass/update/(?P<pk>[0-9]+)/$', views.UserClassUpdate.as_view(), name='user_class_update'),
    url(r'^parent/update/(?P<student_id>[0-9]+)/$', views.UserParentUpdateTemplate.as_view(),
        name='user_parent_update'),
    url(r'^parent/delete/(?P<pk>[0-9]+)/$', views.UserParentDelete.as_view(), name='user_parent_delete'),
    # 组及权限
    url(r'^group/list/$', views.GroupList.as_view(), name='group_list'),
    url(r'^status/save/$', views.StatusSave.as_view(), name='status_save'),
    # 头像
    url(r'^avatar/update/(?P<pk>[0-9]+)/$', views.AvatarUpdate.as_view(), name='avatar_update'),
    url(r'^room/save/$', views.RoomSave.as_view(), name='room_save'),

    # 结课日期
    url(r'^leave/list/(?P<user_id>[0-9]+)/$', views.LeaveList.as_view(), name='leave_list'),
    url(r'^leave/detail/(?P<pk>[0-9]+)/$', views.LeaveDetail.as_view(), name='leave_detail'),
    url(r'^leave/add/(?P<user_id>[0-9]+)/$', views.LeaveCreate.as_view(), name='leave_add'),
    url(r'^leave/check/$', views.LeaveUpdateCheck.as_view(), name='leave_check'),
    url(r'^leave/cancel/(?P<pk>[0-9]+)/$', views.LeaveCancel.as_view(), name='leave_cancel'),
    url(r'^leave/delete/(?P<pk>[0-9]+)/$', views.LeaveDelete.as_view(), name='leave_delete'),

    # 班级
    url(r'^class/list/$', views.ClassList.as_view(), name='class_list'),
    url(r'^class/dashboard/$', views.ClassDashboard.as_view(), name='class_dashboard'),
    url(r'^class/create/$', views.ClassCreate.as_view(), name='class_create'),
    url(r'^class/detail/(?P<pk>[0-9]+)/$', views.ClassDetail.as_view(), name='class_detail'),
    url(r'^class/update/(?P<pk>[0-9]+)/$', views.ClassUpdate.as_view(), name='class_update'),

    # 用户升级
    url(r'^level/list/$', views.LevelList.as_view(), name='level_list'),
    url(r'^level/detail/(?P<pk>[0-9]+)/$', views.LevelDetail.as_view(), name='level_detail'),
    url(r'^level/add/$', views.LevelCreate.as_view(), name='level_add'),
    url(r'^level/update/(?P<pk>[0-9]+)/$', views.LevelUpdate.as_view(), name='level_update'),
    url(r'^level/delete/(?P<pk>[0-9]+)/$', views.LevelDelete.as_view(), name='level_delete'),

    url(r'^level/record/list/(?P<user_id>[0-9]+)/$', views.LevelRecrodList.as_view(), name='level_record_list'),
    url(r'^level/record/detail/(?P<pk>[0-9]+)/$', views.LevelRecrodDetail.as_view(), name='level_record_detail'),
    url(r'^level/record/add/(?P<user_id>[0-9]+)/$', views.LevelRecrodCreate.as_view(), name='level_record_add'),
    url(r'^level/record/update/(?P<pk>[0-9]+)/$', views.LevelRecrodUpdate.as_view(), name='level_record_update'),
    # 用户前台申请列表
    url(r'^custom/level/record/list/(?P<user_id>[0-9]+)/$', views.CustomLevelRecrodList.as_view(),
        name='custom_level_record_list'),
    # 用户提交申请页
    url(r'^custom/level/record/apply/(?P<pk>[0-9]+)/$', views.CustomLevelRecrodApply.as_view(),
        name='custom_level_record_apply'),

    # 权限
    url(r'^permission$', views.UserPermisionList.as_view(), name='user_permission'),
    url(r'^permission/update/(?P<group_id>[0-9]+)/(?P<pk>[0-9]+)$', views.UserPermisionUpdate.as_view(), name='user_permission_update'),
    url(r'^permission/reset/$', views.UserPermisionResetTemplate.as_view(), name='user_permission_reset'),

    # =======微信小程序 ============
    url(r'^wxapp/', include('bee_django_user.wxapp_urls')),
    # =======微信公众号 ============
    url(r'^wxService/user/bind$', views.WxServiceUserBind.as_view(), name='wx_service_user_bind'),
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='bee_django_user/user/login.html'), name='user_login'),
]
