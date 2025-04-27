from django.urls import path
from .views import ProgramListView, ProgramDetailView

app_name = 'programs'

urlpatterns = [
    path('', ProgramListView.as_view(), name='program_list'),
    # URL for listing programs by category
    path('category/<slug:category_slug>/', ProgramListView.as_view(), name='program_list_by_category'),
    # URL for a specific program detail page
    path('<slug:category_slug>/<slug:program_slug>/', ProgramDetailView.as_view(), name='program_detail'),
]