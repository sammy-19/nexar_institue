from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from .models import PageContent
from programs.models import Program, ProgramCategory
from contact.models import ContactMessage
from admissions.models import ApplicationFormField, ApplicationSubmission, ApplicationSubmissionData


# 1. Page Content Management
@admin.register(PageContent)
class PageContentAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'content_type', 'description', 'last_updated')
    list_filter = ('content_type',)
    search_fields = ('identifier', 'description', 'text_content')
    readonly_fields = ('last_updated',)
    fieldsets = (
        (None, {
            'fields': ('identifier', 'description', 'content_type')
        }),
        ('Content (Fill ONE based on Content Type)', {
            'fields': ('text_content', 'image_content'),
        }),
    )

# 2. Program Management (Moved from programs/admin.py)
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

# 3. Contact Message Management (Moved from contact/admin.py)
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'submitted_at', 'is_read')
    list_filter = ('is_read', 'submitted_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'submitted_at')
    list_editable = ('is_read',)
    date_hierarchy = 'submitted_at'
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as Read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Mark selected messages as Unread"

# 4. Application Form Field Management (New)
@admin.register(ApplicationFormField)
class ApplicationFormFieldAdmin(admin.ModelAdmin):
    list_display = ('label', 'field_name', 'field_type', 'order', 'is_required', 'is_active')
    list_editable = ('order', 'is_required', 'is_active')
    list_filter = ('field_type', 'is_required', 'is_active')
    search_fields = ('label', 'field_name', 'help_text')

# 5. Application Submission Management (New)
class ApplicationSubmissionDataInline(admin.TabularInline):
    """Inline view for submission data within the submission admin."""
    model = ApplicationSubmissionData
    extra = 0
    # Make all fields read-only in the inline view
    readonly_fields = ('field', 'display_value') # Use a custom display method
    fields = ('field', 'display_value') # Control field order
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

    @admin.display(description='Submitted Value')
    def display_value(self, obj):
        """Displays the value, rendering a link for files/images."""
        if obj.field.field_type in ['file', 'image'] and obj.value:
            # Assuming obj.value stores the URL path like /media/application_files/...
            file_url = obj.value
            # Optional: Check if it's an image and display a thumbnail
            if obj.field.field_type == 'image':
                return format_html('<a href="{0}" target="_blank"><img src="{0}" height="50" alt="preview"></a> <a href="{0}" target="_blank">Open</a>', file_url)
            else:
                # Just provide a link for other files
                filename = file_url.split('/')[-1]
                return format_html('<a href="{0}" target="_blank">{1}</a>', file_url, filename)
        # For other field types, just display the stored text value
        return obj.value

@admin.register(ApplicationSubmission)
class ApplicationSubmissionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'applicant_name', 'applicant_email', 'submitted_at')
    list_filter = ('submitted_at',)
    search_fields = ('applicant_name', 'applicant_email', 'data__value')
    readonly_fields = ('submitted_at', 'applicant_name', 'applicant_email')
    date_hierarchy = 'submitted_at'
    inlines = [ApplicationSubmissionDataInline]