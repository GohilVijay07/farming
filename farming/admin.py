from django.contrib import admin
from django.db.models import Count
from .models import (
    District,
    Taluka,
    Village,
    FarmerProfile,
    Crop,
    ContactMessage,
    EmailVerificationOTP,
    PasswordResetOTP,
    FarmingTip,
    ActivityLog
)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'taluka_count', 'farmer_count', 'created_at')
    search_fields = ('name', 'region')
    list_filter = ('region',)
    ordering = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _taluka_count=Count('talukas', distinct=True),
            _farmer_count=Count('farmers', distinct=True)
        )

    def taluka_count(self, obj):
        return obj._taluka_count
    taluka_count.short_description = "Talukas"
    taluka_count.admin_order_field = '_taluka_count'

    def farmer_count(self, obj):
        return obj._farmer_count
    farmer_count.short_description = "Registered Farmers"
    farmer_count.admin_order_field = '_farmer_count'


@admin.register(Taluka)
class TalukaAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'village_count', 'farmer_count', 'created_at')
    search_fields = ('name', 'district__name')
    list_filter = ('district__name',)
    ordering = ('district__name', 'name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('district').annotate(
            _village_count=Count('villages', distinct=True),
            _farmer_count=Count('farmers', distinct=True)
        )

    def village_count(self, obj):
        return obj._village_count
    village_count.short_description = "Villages"
    village_count.admin_order_field = '_village_count'

    def farmer_count(self, obj):
        return obj._farmer_count
    farmer_count.short_description = "Farmers"
    farmer_count.admin_order_field = '_farmer_count'


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'taluka', 'get_district', 'pincode', 'created_at')
    search_fields = ('name', 'taluka__name', 'taluka__district__name', 'pincode')
    list_filter = ('taluka__district__name',)
    ordering = ('taluka__district__name', 'taluka__name', 'name')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('taluka__district')

    def get_district(self, obj):
        return obj.taluka.district.name if obj.taluka and obj.taluka.district else "-"
    get_district.short_description = "District"
    get_district.admin_order_field = 'taluka__district__name'


@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'district', 'taluka', 'farm_location', 'created_at')
    search_fields = ('user__username', 'full_name', 'phone', 'district', 'taluka', 'farm_location')
    list_filter = ('district', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    select_related = ('user', 'district_ref', 'taluka_ref', 'village_ref')


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('crop_name', 'farmer', 'crop_type', 'district', 'taluka', 'farm_area', 'status', 'planting_date', 'expected_harvest_date')
    list_filter = ('status', 'district', 'season', 'crop_type', 'created_at')
    search_fields = ('crop_name', 'farmer__username', 'district', 'taluka', 'village', 'notes')
    date_hierarchy = 'planting_date'
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    select_related = ('farmer', 'district_ref', 'taluka_ref', 'village_ref')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'is_read', 'read_at', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('status', 'is_read', 'created_at')
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
