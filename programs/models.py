from django.db import models
from django.urls import reverse
# Create your models here.


class ProgramCategory(models.Model):
    """Represents a category of programs (e.g., Diploma, Certificate)."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, help_text="URL-friendly version of the name")

    class Meta:
        verbose_name_plural = "Program Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Program(models.Model):
    """Represents an academic program offered by the institute."""
    category = models.ForeignKey(ProgramCategory, on_delete=models.PROTECT, related_name='programs')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210, unique=True, help_text="URL-friendly version of the title")
    description = models.TextField(blank=True, help_text="Detailed description of the program.")
    duration = models.CharField(max_length=100, help_text="e.g., 3 Years, 6 Months")
    # Add more fields as needed: prerequisites, curriculum_details, learning_outcomes, image, etc.
    is_active = models.BooleanField(default=True, help_text="Is this program currently offered?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['category', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this program."""
        return reverse('programs:program_detail', kwargs={'category_slug': self.category.slug, 'program_slug': self.slug})
