from django.contrib import admin
from .models import FarmerProfile, Crop, ContactMessage, EmailVerificationOTP, PasswordResetOTP, FarmingTip, ActivityLog


@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'farm_location', 'created_at')
    search_fields = ('user__username', 'full_name', 'phone', 'farm_location')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('crop_name', 'farmer', 'crop_type', 'season', 'farm_area', 'status', 'planting_date', 'expected_harvest_date')
    list_filter = ('status', 'season', 'crop_type', 'created_at')
    search_fields = ('crop_name', 'farmer__username', 'notes', 'season')
    date_hierarchy = 'planting_date'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'read_at', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('is_read', 'created_at')
    readonly_fields = ('created_at', 'read_at')
    ordering = ('-created_at',)


@admin.register(EmailVerificationOTP)
class EmailVerificationOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'expires_at', 'is_verified', 'attempts')
    list_filter = ('is_verified', 'created_at', 'expires_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('user', 'otp_hash', 'created_at', 'expires_at', 'is_verified', 'attempts')
    ordering = ('-created_at',)


@admin.register(PasswordResetOTP)
class PasswordResetOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'expires_at', 'is_verified', 'attempts')
    list_filter = ('is_verified', 'created_at', 'expires_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('user', 'otp_hash', 'created_at', 'expires_at', 'is_verified', 'attempts')
    ordering = ('-created_at',)


@admin.register(FarmingTip)
class FarmingTipAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'level', 'created_at', 'updated_at')
    list_filter = ('category', 'level', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('category', '-created_at')


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'details', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('action', 'details', 'user__username')
    readonly_fields = ('user', 'action', 'details', 'icon', 'created_at')
    ordering = ('-created_at',)

