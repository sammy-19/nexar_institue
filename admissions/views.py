from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import DynamicApplicationForm
from .models import ApplicationFormField

# Create your views here.

class AdmissionsInfoView(TemplateView):
    template_name = "admissions/info.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Admissions Information'
        context['enrollment_process'] = """
        Prospective students embark on their academic journey at Nexar Institute by meticulously
        preparing and submitting applications. These applications undergo a thorough review process, with
        a keen focus on academic qualifications and other pertinent criteria. Upon acceptance, students are
        welcomed into the institute through an orientation program... (Add more from profile)
        """
        context['target_market'] = "Our primary target market includes Zambian youth and young graduates seeking quality education and employment opportunities."
        # Add more context about assessment, etc.
        return context
    
class ApplicationFormView(FormView):
    template_name = 'admissions/application_form.html'
    form_class = DynamicApplicationForm
    success_url = reverse_lazy('admissions:application_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Online Application'
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid. Pass request.FILES.
        """
        form = self.get_form_class()(request.POST, request.FILES) # Pass request.FILES here
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        try:
            # Pass request.FILES to the save method
            form.save(files_data=self.request.FILES)
            messages.success(self.request, 'Your application has been submitted successfully!')
        except Exception as e:
            messages.error(self.request, f'There was an error submitting your application: {e}. Please try again.')
            print(f"Error saving application: {e}")
            return self.form_invalid(form)

        return super().form_valid(form) # Redirects to success_url

    def form_invalid(self, form):
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

class ApplicationSuccessView(TemplateView):
    template_name = 'admissions/application_success.html'
    # ... (get_context_data remains the same) ...
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Application Submitted'
        return context
