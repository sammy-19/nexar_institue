from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = "core/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Welcome to Nexar Institute'
        # Add more context from the profile if needed
        return context

class AboutUsView(TemplateView):
    template_name = "core/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'About Us'
        # Add context about background, objectives, commitment etc.
        context['background'] = """
        Nexar Institute of Health Sciences and Business Studies is a registered health sciences-based
        learning and training institute whose mission is to offer high quality education and skills necessary
        for our students to assure optimum health conditions in the community and beyond... (Add more from profile)
        """
        context['objectives'] = [
            "To bridge the skills gap in healthcare and business sectors by offering education and practical training.",
            "To provide equitable access to quality education in health sciences and business studies by expanding to provincial towns.",
            "To stimulate entrepreneurship to empower students to drive economic growth and innovation in Zambia.",
            "To produce ethically responsible professionals who uphold integrity and ethical standards in healthcare and business sectors."
        ]
        return context

class MissionVisionView(TemplateView):
    template_name = "core/mission_vision.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Mission & Vision'
        context['vision'] = """
        Nexar Institute envisions a dynamic future where excellence in
        education and practical skills meet to redefine success in healthcare
        and business. We aspire to be the catalyst for transformative growth,
        producing ethical leaders, fostering innovation, and driving Zambia's
        prosperity and sustainability on a global stage.
        """
        context['mission'] = """
        Offer high quality education and skills necessary for students to assure optimum health
        conditions in the community and beyond. Narrowing skill gaps in healthcare and business
        while democratizing access to quality learning to pioneer economic growth, human
        development and innovation.
        """
        return context