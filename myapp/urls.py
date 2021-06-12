"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index2'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),

    path('district_list_view', views.district_list_view, name='district_list_view'),
    path('block_list_view', views.block_list_view, name='block_list_view'),
    path('panchayat_list_view', views.panchayat_list_view, name='panchayat_list_view'),

    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_changepassword', views.admin_changepassword, name='admin_changepassword'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_home', views.admin_home, name='admin_home'),

    path('admin_state_settings_add', views.admin_state_settings_add, name='admin_state_settings_add'),
    path('admin_state_settings_edit', views.admin_state_settings_edit, name='admin_state_settings_edit'),
    path('admin_state_settings_view', views.admin_state_settings_view, name='admin_state_settings_view'),
    path('admin_state_settings_delete', views.admin_state_settings_delete, name='admin_state_settings_delete'),

    path('admin_district_settings_add', views.admin_district_settings_add, name='admin_district_settings_add'),
    path('admin_district_settings_edit', views.admin_district_settings_edit, name='admin_district_settings_edit'),
    path('admin_district_settings_view', views.admin_district_settings_view, name='admin_district_settings_view'),
    path('admin_district_settings_delete', views.admin_district_settings_delete, name='admin_district_settings_delete'),

    path('admin_block_settings_add', views.admin_block_settings_add, name='admin_block_settings_add'),
    path('admin_block_settings_edit', views.admin_block_settings_edit, name='admin_block_settings_edit'),
    path('admin_block_settings_view', views.admin_block_settings_view, name='admin_block_settings_view'),
    path('admin_block_settings_delete', views.admin_block_settings_delete, name='admin_block_settings_delete'),

    path('admin_panchayat_settings_add', views.admin_panchayat_settings_add, name='admin_panchayat_settings_add'),
    path('admin_panchayat_settings_add2', views.admin_panchayat_settings_add2, name='admin_panchayat_settings_add2'),
    path('admin_panchayat_settings_edit', views.admin_panchayat_settings_edit, name='admin_panchayat_settings_edit'),
    path('admin_panchayat_settings_view', views.admin_panchayat_settings_view, name='admin_panchayat_settings_view'),
    path('admin_panchayat_settings_delete', views.admin_panchayat_settings_delete, name='admin_panchayat_settings_delete'),


    path('panchayat_login', views.panchayat_login, name='panchayat_login'),
    path('panchayat_changepassword', views.panchayat_changepassword, name='panchayat_changepassword'),
    path('panchayat_logout', views.panchayat_logout, name='panchayat_logout'),
    path('panchayat_home', views.panchayat_home, name='panchayat_home'),

    path('panchayat_panchayat_settings_edit', views.panchayat_panchayat_settings_edit, name='panchayat_panchayat_settings_edit'),

    path('panchayat_ward_member_add', views.panchayat_ward_member_add, name='panchayat_ward_member_add'),
    path('panchayat_ward_member_edit', views.panchayat_ward_member_edit, name='panchayat_ward_member_edit'),
    path('panchayat_ward_member_view', views.panchayat_ward_member_view, name='panchayat_ward_member_view'),
    path('panchayat_ward_member_delete', views.panchayat_ward_member_delete, name='panchayat_ward_member_delete'),
    path('panchayat_ward_member_search', views.panchayat_ward_member_search, name='panchayat_ward_member_search'),

    path('panchayat_news_add', views.panchayat_news_add, name='panchayat_news_add'),
    path('panchayat_news_view', views.panchayat_news_view, name='panchayat_news_view'),
    path('panchayat_request_edit', views.panchayat_request_edit, name='panchayat_request_edit'),

    path('panchayat_user_tax_view', views.panchayat_user_tax_view, name='panchayat_user_tax_view'),

    path('panchayat_user_messages_view', views.panchayat_user_messages_view, name='panchayat_user_messages_view'),
    path('panchayat_user_messages_reply',views.panchayat_user_messages_reply,name='panchayat_user_messages_reply'),
    path('panchayat_user_licence_request_view', views.panchayat_user_licence_request_view, name='panchayat_user_licence_request_view'),

    path('ward_login', views.ward_login, name='ward_login'),
    path('ward_changepassword', views.ward_changepassword, name='ward_changepassword'),
    path('ward_logout', views.ward_logout, name='ward_logout'),
    path('ward_home', views.ward_home, name='ward_home'),

    path('ward_member_details_edit', views.ward_member_details_edit,name='ward_member_details_edit'),

    path('ward_member_search', views.ward_member_search, name='ward_member_search'),
    path('ward_user_search', views.ward_user_search, name='ward_user_search'),

    path('ward_panchayat_news_view',views.ward_panchayat_news_view,name='ward_panchayat_news_view'),

    path('ward_news_add', views.ward_news_add, name='ward_news_add'),
    path('ward_news_view', views.ward_news_view, name='ward_news_view'),
    path('ward_news_delete', views.ward_news_delete, name='ward_news_delete'),

    path('ward_covid_add', views.ward_covid_add, name='ward_covid_add'),
    path('ward_covid_view', views.ward_covid_view, name='ward_covid_view'),
    path('ward_covid_edit', views.ward_covid_edit, name='ward_covid_edit'),
    path('ward_covid_delete', views.ward_covid_delete, name='ward_covid_delete'),

    path('ward_user_messages_view', views.ward_user_messages_view, name='ward_user_messages_view'),
    path('ward_user_messages_reply', views.ward_user_messages_reply, name='ward_user_messages_reply'),

    path('ward_panchayat_settings_view', views.ward_panchayat_settings_view, name='ward_panchayat_settings_view'),

    path('user_login', views.user_login_check, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('user_home', views.user_home, name='user_home'),
    path('user_details_add', views.user_details_add, name='user_details_add'),
    path('user_details_edit', views.user_details_edit, name='user_details_edit'),
    path('user_changepassword', views.user_changepassword, name='user_changepassword'),

    path('user_ward_member_search', views.user_ward_member_search, name='user_ward_member_search'),
    path('user_ward_news_view', views.user_ward_news_view, name='user_ward_news_view'),
    path('user_panchayat_news_view', views.user_panchayat_news_view, name='user_panchayat_news_view'),
    path('user_ward_covid_view', views.user_ward_covid_view, name='user_ward_covid_view'),

    path('user_panchayat_messages_add', views.user_panchayat_messages_add, name='user_panchayat_messages_add'),
    path('user_panchayat_messages_view', views.user_panchayat_messages_view, name='user_panchayat_messages_view'),

    path('user_ward_messages_add', views.user_ward_messages_add, name='user_ward_messages_add'),
    path('user_ward_messages_view', views.user_ward_messages_view, name='user_ward_messages_view'),

    path('user_tax_add', views.user_tax_add, name='user_tax_add'),
    path('user_tax_view', views.user_tax_view, name='user_tax_view'),
    path('admin_tax_verify', views.admin_tax_verify, name='admin_tax_verify'),
    path('user_tax_pay', views.user_tax_pay, name='user_tax_pay'),
    path('user_tax_payment', views.user_tax_payment, name='user_tax_payment'),

    path('user_panchayat_settings_view',views.user_panchayat_settings_view,name='user_panchayat_settings_view'),

    path('user_licence_request_add', views.user_licence_request_add, name='user_licence_request_add'),
    path('user_licence_request_delete', views.user_licence_request_delete, name='user_licence_request_delete'),
    path('user_licence_request_view', views.user_licence_request_view, name='user_licence_request_view'),

    path('export_pdf', views.export_pdf, name='export_pdf'),
    path('invoice_pdf', views.invoice_pdf, name='invoice_pdf'),

]
