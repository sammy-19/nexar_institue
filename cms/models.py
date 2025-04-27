from django.db import models

# Create your models here.
class PageContent(models.Model):
    """Model to store manageable content snippets for pages."""
    CONTENT_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('rich_text', 'Rich Text'), # Consider using django-ckeditor or similar
    ]

    identifier = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique identifier for this content (e.g., 'programs_banner', 'about_us_intro')."
    )
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES, default='text')
    text_content = models.TextField(blank=True, null=True, help_text="Use for plain text or rich text content.")
    image_content = models.ImageField(
        upload_to='page_content_images/', # Files will be saved in MEDIA_ROOT/page_content_images/
        blank=True,
        null=True,
        help_text="Use for image content."
    )
    description = models.CharField(max_length=255, blank=True, help_text="Brief description of what this content is for.")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.identifier

    def get_content(self):
        """Helper method to return the appropriate content based on type."""
        if self.content_type == 'image' and self.image_content:
            return self.image_content.url
        elif self.content_type in ['text', 'rich_text']:
            return self.text_content
        return None