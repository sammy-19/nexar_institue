from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm

class ContactView(FormView):
    template_name = 'contact/contact_page.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact:success') # Redirect to a success page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Contact Us'
        # Add contact details from profile
        context['address'] = "Ninth Floor Kulima Tower Building, Katunjila Road, Lusaka, Zambia"
        context['email'] = "nexarschool@gmail.com"
        context['phone'] = "+260767814141"
        context['po_box'] = "PO Box 31568 Lusaka, Zambia"
        # Optional: Add Google Maps embed code here if desired
        return context

    def form_valid(self, form):
        # Save the message to the database
        contact_message = form.save()

        # Send an email notification (optional, requires email backend setup)
        try:
            subject = f"New Contact Form Submission: {contact_message.subject}"
            message_body = f"""
            You received a new message from the website contact form:

            Name: {contact_message.name}
            Email: {contact_message.email}
            Subject: {contact_message.subject}
            Message:
            {contact_message.message}

            Submitted At: {contact_message.submitted_at.strftime('%Y-%m-%d %H:%M:%S %Z')}
            """
            send_mail(
                subject,
                message_body,
                settings.DEFAULT_FROM_EMAIL, # From email
                [settings.ADMIN_EMAIL],      # To email(s) - replace with actual admin email
                fail_silently=False,
            )
            messages.success(self.request, 'Your message has been sent successfully!')
        except Exception as e:
            # Handle email sending errors gracefully
            messages.error(self.request, f'There was an error sending your message: {e}. Please try again later.')
            # Optionally log the error: import logging; logger = logging.getLogger(__name__); logger.error(f"Email send failed: {e}")
            # Still redirect to success page, but maybe show a different message there
            pass # Continue to success URL even if email fails, as message is saved

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class ContactSuccessView(TemplateView):
    template_name = 'contact/contact_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Message Sent'
        return context