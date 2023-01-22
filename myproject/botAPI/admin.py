from django.contrib import admin

from botAPI.models import CustomUser, Space, SpendingCategory, Spending, ReferralCode, SpaceLog, PersonStatus

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'telegram_id', 'created_at')
    list_display_links = ('id', 'name')


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'currency', 'created_at', 'cost_amount')
    list_display_links = ('id', 'title')


@admin.register(SpendingCategory)
class SpendingCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'space', 'created_at')
    list_display_links = ('id', 'title')


@admin.register(Spending)
class SpendingAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'user', 'expense', 'currency', 'space', 'created_at')


@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'space', 'expiration_time', 'created_at')
    list_display_links = ('id', 'code')


@admin.register(SpaceLog)
class SpaceLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'action', 'user', 'created_at')
    list_display_links = ('id', 'action')



@admin.register(PersonStatus)
class PersonStatusAdmin(admin.ModelAdmin):
    pass
