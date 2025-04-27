from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Program, ProgramCategory

# Create your views here.

class ProgramListView(ListView):
    """Displays a list of all active programs, optionally filtered by category."""
    model = Program
    template_name = 'programs/program_list.html'
    context_object_name = 'programs'

    def get_queryset(self):
        """Filter programs by active status and optionally by category."""
        queryset = Program.objects.filter(is_active=True).select_related('category')
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(ProgramCategory, slug=category_slug)
            queryset = queryset.filter(category=category)
            self.category = category # Store category for context
        else:
            self.category = None
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Our Programs'
        context['categories'] = ProgramCategory.objects.all()
        context['current_category'] = self.category
        # Populate with initial data from profile (can be moved to fixtures later)
        if not Program.objects.exists():
             self._create_initial_programs()
        return context

    def _create_initial_programs(self):
        """Helper to create initial programs if DB is empty."""
        diploma_cat, _ = ProgramCategory.objects.get_or_create(name='Diploma Programs', slug='diploma-programs')
        cert_cat, _ = ProgramCategory.objects.get_or_create(name='Certificate Programs', slug='certificate-programs')

        diploma_programs = [
            ('Clinical Medicine', 'clinical-medicine', '3 Years'),
            ('Environmental Health', 'environmental-health', '3 Years'),
            ('Business Administration', 'business-administration', '3 Years'),
            ('Nursing', 'nursing', '3 Years'),
            ('Public Health', 'public-health', '3 Years'),
            ('Occupational Health and Safety', 'occupational-health-safety', '3 Years'),
            ('Pharmacy', 'pharmacy', '3 Years'),
            ('Nutrition', 'diploma-nutrition', '3 Years'), # Different slug for uniqueness
        ]
        cert_programs = [
            ('Nursing Assistant', 'nursing-assistant', '6 Months'),
            ('Psychosocial Counselling', 'psychosocial-counselling', '6 Months'),
            ('Mental Health', 'mental-health', '6 Months'),
            ('Health Care Assistant', 'health-care-assistant', '6 Months'),
            ('HIV/AIDS Management', 'hiv-aids-management', '6 Months'),
            ('Nutrition', 'certificate-nutrition', '6 Months'), # Different slug for uniqueness
        ]

        for title, slug, duration in diploma_programs:
            Program.objects.get_or_create(
                category=diploma_cat, title=title, slug=slug, duration=duration,
                defaults={'description': f'Details about the {title} program.'}
            )
        for title, slug, duration in cert_programs:
             Program.objects.get_or_create(
                category=cert_cat, title=title, slug=slug, duration=duration,
                defaults={'description': f'Details about the {title} program.'}
            )


class ProgramDetailView(DetailView):
    """Displays details for a single program."""
    model = Program
    template_name = 'programs/program_detail.html'
    context_object_name = 'program'
    slug_url_kwarg = 'program_slug' # Matches the URL pattern parameter

    def get_queryset(self):
        """Ensure we only fetch active programs and filter by category slug."""
        return Program.objects.filter(is_active=True, category__slug=self.kwargs.get('category_slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.object.title
        return context
