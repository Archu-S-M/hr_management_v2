from django.conf.urls import url

from .views import *


urlpatterns = [
    url(r'Dashboard/',Dashboard.as_view(),name="Dashboard"),
    url(r'ManageConsultancy/',ManageConsultancy.as_view(),name="ManageConsultancy"),
    url(r'CandidateProfile/',CandidateProfile.as_view(),name="CandidateProfile"),
    url(r'Questionnaire/',Questionnaire.as_view(),name="Questionnaire"),
    url(r'Requirements/',Requirements.as_view(),name="Requirements"),
    url(r'Settings/',Dashboard.as_view(),name="Settings"),
]