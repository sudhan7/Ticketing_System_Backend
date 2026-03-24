from django.urls import path
from issues import views

urlpatterns = [
    path('api/issues/', views.create_issue, name='create_issue'),
    path('api/issues/all/', views.get_issues, name='get_issues'),
    path('api/issues/<int:issue_id>/', views.get_issue_by_id, name='get_issue_by_id'),
    path('api/issues/status/<str:status>/', views.get_issues_by_status, name='get_issues_by_status'),
    path('api/reporters/', views.create_reporter, name='create_reporter'),
    path('api/reporters/all/', views.get_reporters, name='get_reporters'),
    path('api/reporters/<int:reporter_id>/', views.get_reporter_by_id, name='get_reporter_by_id'),
]
