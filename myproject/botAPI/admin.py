from django.contrib import admin

from botAPI.models import CustomUser, Space, SpendingCategory, Spending, ReferralCode, SpaceLog, PersonStatus


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    pass


@admin.register(SpendingCategory)
class SpendingCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Spending)
class SpendingAdmin(admin.ModelAdmin):
    pass


@admin.register(ReferralCode)
class ReferralCodeAdmin(admin.ModelAdmin):
    pass


@admin.register(SpaceLog)
class SpaceLogAdmin(admin.ModelAdmin):
    pass



@admin.register(PersonStatus)
class PersonStatusAdmin(admin.ModelAdmin):
    pass
