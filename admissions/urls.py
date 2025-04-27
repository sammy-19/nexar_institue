from django.urls import path
from .views import AdmissionsInfoView, ApplicationFormView, ApplicationSuccessView 

app_name = 'admissions' # Namespace

urlpatterns = [
    path('', AdmissionsInfoView.as_view(), name='info'),
    path('apply/', ApplicationFormView.as_view(), name='application_form'),
    path('apply/success/', ApplicationSuccessView.as_view(), name='application_success'),
]
