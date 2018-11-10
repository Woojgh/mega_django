from django.contrib import admin
from . import models

@admin.register(models.UserProfile)
class ExerciseAdmin(admin.ModelAdmin):
    # search_fields = ('owner', 'name', 'description',)
    # list_filter = ('is_public', 'is_refused')
    list_display = ('pk', 'uuid_photo', 'uuid_cover', 'user', 'photo', 'cover_photo', 'phone_number', 'address', 'zip_code', 'city', 'state', 'country')
    # inlines = (NutritionPlanMealAdminInline,)