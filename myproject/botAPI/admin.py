from django.contrib import admin

from botAPI.models import CustomUser, Space, SpendingCategory, Spending, ReferralCode, SpaceLog, PersonStatus

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'telegram_id', 'created_at')
    list_display_links = ('id', 'name')
    fields = ('name', 'telegram_id', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'currency', 'created_at', 'cost_amount')
    list_display_links = ('id', 'title')
    fields = ('title', 'currency', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(SpendingCategory)
class SpendingCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'space', 'created_at')
    list_display_links = ('id', 'title')
    fields = ('title', 'space', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Spending)
class SpendingAdmin(admin.ModelAdmin):
    list_display = ('id', 'category', 'user', 'expense', 'currency', 'space', 'created_at')
    list_display_links = ('id', 'category')
    fields = ('category', 'user', 'expense', 'currency', 'space', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'space', 'expiration_time', 'created_at')
    list_display_links = ('id', 'code')
    fields = ('code', 'expiration_time', 'user', 'space', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(SpaceLog)
class SpaceLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'action', 'user', 'created_at')
    list_display_links = ('id', 'action')
    fields = ('user', 'action', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(PersonStatus)
class PersonStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'space', 'grade', 'is_banned', 'created_at')
    list_display_links = ('id', 'user')
    fields = ('user', 'space', 'grade', 'is_banned', 'created_at')
    readonly_fields = ('created_at',)

admin.site.site_title = 'Админ-панель для FamilyFinanceBot'
admin.site.site_header = 'Админ-панель для FamilyFinanceBot'