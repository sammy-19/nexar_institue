from django.shortcuts import render
from django.views.generic import TemplateView

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