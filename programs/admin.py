from django.contrib import admin
# from .models import ProgramCategory, Program

# Register your models here.
"""
@admin.register(ProgramCategory)
class ProgramCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'duration', 'is_active', 'updated_at')
    list_filter = ('category', 'is_active', 'duration')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active',)
    date_hierarchy = 'created_at'
"""