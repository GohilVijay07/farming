from django.urls import path
from . import views

urlpatterns = [
    # Public Pages
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('crops/', views.crops_view, name='crops'),
    path('farming-tips/', views.farming_tips_view, name='farming_tips'),
    path('weather/', views.weather_view, name='weather'),
    path('api/weather/', views.api_weather_view, name='api_weather'),
    path('contact/', views.contact_view, name='contact'),

    # Location Dependent Dropdown JSON APIs
    path('api/districts/', views.api_districts_view, name='api_districts'),
    path('api/talukas/', views.api_talukas_view, name='api_talukas'),
    path('api/villages/', views.api_villages_view, name='api_villages'),

    # Authentication & Registration OTP Verification
    path('register/', views.register_view, name='register'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Forgot Password & Password Reset via 6-Digit Email OTP
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('forgot-password/verify-otp/', views.verify_password_reset_otp_view, name='verify_password_reset_otp'),
    path('forgot-password/resend-otp/', views.resend_password_reset_otp_view, name='resend_password_reset_otp'),
    path('forgot-password/reset/', views.reset_password_view, name='reset_password'),
    path('forgot-password/success/', views.password_reset_success_view, name='password_reset_success'),

    # Farmer Management Portal (Login Required)
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('my-crops/', views.my_crops_view, name='my_crops'),
    path('add-crop/', views.add_crop_view, name='add_crop'),
    path('edit-crop/<int:id>/', views.edit_crop_view, name='edit_crop'),
    path('delete-crop/<int:id>/', views.delete_crop_view, name='delete_crop'),
    path('profile/', views.profile_view, name='profile'),

    # ==========================================
    # AGRI-CONNECT ADMIN MANAGEMENT PORTAL
    # ==========================================
    path('admin-login/', views.admin_login_view, name='admin_login'),
    path('admin-logout/', views.admin_logout_view, name='admin_logout'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    
    # Admin User Management
    path('admin-dashboard/users/', views.admin_users_view, name='admin_users'),
    path('admin-dashboard/users/<int:id>/', views.admin_user_detail_view, name='admin_user_detail'),
    path('admin-dashboard/users/<int:id>/edit/', views.admin_user_edit_view, name='admin_user_edit'),
    path('admin-dashboard/users/<int:id>/toggle-status/', views.admin_user_toggle_status_view, name='admin_user_toggle_status'),
    path('admin-dashboard/users/<int:id>/delete/', views.admin_user_delete_view, name='admin_user_delete'),
    
    # Admin Crop Management
    path('admin-dashboard/crops/', views.admin_crops_view, name='admin_crops'),
    path('admin-dashboard/crops/<int:id>/edit/', views.admin_crop_edit_view, name='admin_crop_edit'),
    path('admin-dashboard/crops/<int:id>/delete/', views.admin_crop_delete_view, name='admin_crop_delete'),
    
    # Admin Contact Messages
    path('admin-dashboard/messages/', views.admin_messages_view, name='admin_messages'),
    path('admin-dashboard/messages/<int:id>/', views.admin_message_detail_view, name='admin_message_detail'),
    path('admin-dashboard/messages/<int:id>/toggle-read/', views.admin_message_toggle_read_view, name='admin_message_toggle_read'),
    path('admin-dashboard/messages/<int:id>/delete/', views.admin_message_delete_view, name='admin_message_delete'),
    
    # Admin OTP Verification
    path('admin-dashboard/otp/', views.admin_otp_view, name='admin_otp'),
    path('admin-dashboard/otp/resend/<int:user_id>/', views.admin_resend_otp_view, name='admin_resend_otp'),
    
    # Admin Farming Tips Management
    path('admin-dashboard/tips/', views.admin_tips_view, name='admin_tips'),
    path('admin-dashboard/tips/add/', views.admin_tip_add_view, name='admin_tip_add'),
    path('admin-dashboard/tips/<int:id>/edit/', views.admin_tip_edit_view, name='admin_tip_edit'),
    path('admin-dashboard/tips/<int:id>/delete/', views.admin_tip_delete_view, name='admin_tip_delete'),
    
    # Admin Weather, Analytics, Activity
    path('admin-dashboard/weather/', views.admin_weather_view, name='admin_weather'),
    path('admin-dashboard/analytics/', views.admin_analytics_view, name='admin_analytics'),
    path('admin-dashboard/activity/', views.admin_activity_view, name='admin_activity'),
]
