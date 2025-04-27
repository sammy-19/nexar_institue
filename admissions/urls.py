from django.urls import path
from .views import AdmissionsInfoView

app_name = 'admissions' # Namespace

urlpatterns = [
    path('', AdmissionsInfoView.as_view(), name='info'),
]
