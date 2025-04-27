from django.urls import path
from .views import HomePageView, AboutUsView, MissionVisionView

app_name = 'core'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutUsView.as_view(), name='about'),
    path('mission-vision/', MissionVisionView.as_view(), name='mission_vision'),
]