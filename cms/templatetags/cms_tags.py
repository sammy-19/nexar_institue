from django import template
from cms.models import PageContent
from contact.models import ContactMessage # Import ContactMessage
from django.utils.safestring import mark_safe
from django.urls import reverse # Needed for admin url lookup

register = template.Library()

@register.simple_tag
def get_page_content(identifier, default=""):
    """
    Template tag to retrieve content from PageContent model.
    Usage: {% get_page_content 'identifier_name' as variable_name %}
           {% get_page_content 'identifier_name' %}
    """
    try:
        content_obj = PageContent.objects.get(identifier=identifier)
        content = content_obj.get_content()
        if content_obj.content_type == 'rich_text':
            return mark_safe(content or default)
        return content or default
    except PageContent.DoesNotExist:
        return default
    except Exception:
        return default

@register.simple_tag
def get_image_url(identifier, default_static_path=None):
    
    try:
        content_obj = PageContent.objects.get(identifier=identifier, content_type='image')
        if content_obj.image_content:
            return content_obj.image_content.url
    except PageContent.DoesNotExist:
        pass
    except Exception:
        pass

    if default_static_path:
        from django.templatetags.static import static
        try:
            return static(default_static_path)
        except Exception:
             return ""
    return ""

# --- NEW TEMPLATE TAG ---
@register.simple_tag
def get_unread_message_count():
    """Returns the count of unread ContactMessage objects."""
    try:
        return ContactMessage.objects.filter(is_read=False).count()
    except Exception:
        # Handle potential errors, e.g., if the model doesn't exist yet
        return 0

# --- NEW HELPER TAG FOR ADMIN URLS ---
@register.simple_tag
def get_admin_url(model_instance_or_string):
    """
    Returns the admin change list URL for a given model or 'app_label.model_name' string.
    Usage: {% get_admin_url 'programs.Program' %} or {% get_admin_url program_instance %}
    """
    from django.contrib.contenttypes.models import ContentType
    try:
        if isinstance(model_instance_or_string, str):
            app_label, model_name = model_instance_or_string.lower().split('.')
            # Use ContentType framework to be more robust
            # ct = ContentType.objects.get(app_label=app_label, model=model_name)
            # return reverse(f'admin:{ct.app_label}_{ct.model}_changelist')
            # Simpler approach using string formatting (less robust if model names change case)
            return reverse(f'admin:{app_label}_{model_name}_changelist')
        else:
            # If an instance is passed, get its meta info
            app_label = model_instance_or_string._meta.app_label
            model_name = model_instance_or_string._meta.model_name
            return reverse(f'admin:{app_label}_{model_name}_changelist')
    except Exception:
        # Handle cases where the URL can't be reversed (e.g., model not registered)
        return '#' # Return a safe fallback URL
