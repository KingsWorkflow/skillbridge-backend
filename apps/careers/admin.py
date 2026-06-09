from django.contrib import admin
from .models import CareerPath


@admin.register(CareerPath)
class CareerPathAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'average_salary', 'growth_outlook', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description', 'category')
    filter_horizontal = ('required_skills',)
