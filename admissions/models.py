from django.db import models
from django.utils.translation import gettext_lazy as _

class ApplicationFormField(models.Model):
    """Defines a field available for the dynamic application form."""
    FIELD_TYPE_CHOICES = [
        ('text', 'Text (Single Line)'),
        ('textarea', 'Text Area (Multi Line)'),
        ('email', 'Email'),
        ('number', 'Number'),
        ('select', 'Dropdown Select'),
        ('checkbox', 'Checkbox'),
        ('radio', 'Radio Buttons'),
        ('date', 'Date'),
        ('file', 'File Upload'), # Added File type
        ('image', 'Image Upload'), # Added Image type
    ]

    label = models.CharField(max_length=255, help_text="Text displayed for the form field.")
    field_name = models.SlugField(max_length=100, unique=True, help_text="Internal name for the field (no spaces, e.g., 'first_name').")
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES)
    help_text = models.CharField(max_length=255, blank=True, help_text="Optional help text displayed with the field.")
    choices = models.TextField(blank=True, help_text="For 'select' or 'radio' types, enter choices separated by commas (e.g., Male,Female,Other).")
    is_required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Order in which fields appear on the form.")
    is_active = models.BooleanField(default=True, help_text="Include this field in the form?")

    class Meta:
        ordering = ['order', 'label']
        verbose_name = "Application Form Field"
        verbose_name_plural = "Application Form Fields"

    def __str__(self):
        return self.label

    def get_choices_list(self):
        """Returns choices as a list for select/radio fields."""
        if self.field_type in ['select', 'radio'] and self.choices:
            return [(choice.strip(), choice.strip()) for choice in self.choices.split(',')]
        return []

class ApplicationSubmission(models.Model):
    """Represents a submitted application."""
    applicant_name = models.CharField(max_length=200, blank=True)
    applicant_email = models.EmailField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Application Submission"
        verbose_name_plural = "Application Submissions"

    def __str__(self):
        return f"Submission by {self.applicant_name or self.applicant_email or 'Unknown'} at {self.submitted_at.strftime('%Y-%m-%d %H:%M')}"

class ApplicationSubmissionData(models.Model):
    """Stores the actual data for each field within a submission."""
    submission = models.ForeignKey(ApplicationSubmission, on_delete=models.CASCADE, related_name='data')
    field = models.ForeignKey(ApplicationFormField, on_delete=models.PROTECT)
    # Value still stored as text - will contain file path for file/image fields
    value = models.TextField()

    class Meta:
        unique_together = ('submission', 'field')
        verbose_name = "Submission Data"
        verbose_name_plural = "Submission Data"

    def __str__(self):
        # Truncate value for display
        display_value = self.value
        if self.field.field_type in ['file', 'image'] and self.value:
             # Show only filename for brevity
             try:
                 display_value = self.value.split('/')[-1]
             except:
                 pass # Keep original value if split fails
        elif len(self.value) > 50:
            display_value = self.value[:50] + '...'
        return f"{self.field.label}: {display_value}"