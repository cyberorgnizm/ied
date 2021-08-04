from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('lga/<int:lga_id>/', views.LGAResultView.as_view(), name='lga-results'),
    path('units/<int:uniqueid>/', views.PollingUniteResultView.as_view(), name='unit-results'),
    path('units/<int:uniqueid>/record', views.RecordPollResult.as_view(), name='record-poll'),
]