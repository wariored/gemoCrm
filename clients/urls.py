from django.urls import path

from . import views

app_name = 'clients'
urlpatterns = [
    path('', views.client_index, name='client-index'),
    path('hackers/import', views.import_from_greenhouse, name='client-import'),
    # hacker path
    path('hackers/create', views.CreateHackerView.as_view(), name='create-hacker'),
    path('hackers/<int:pk>/update', views.HackerUpdateView.as_view(), name='update-hacker'),
    path('hackers/list', views.HackerListView.as_view(), name='list-hacker'),
    path('hackers/<int:pk>', views.HackerDetailView.as_view(), name='detail-hacker'),
    # startup path
    path('startups/create', views.StartupCreateView.as_view(), name='create-startup'),
    path('startups/<int:pk>/update', views.StartupUpdateView.as_view(), name='update-startup'),
    path('startups/list', views.StartupListView.as_view(), name='list-startup'),
    path('startups/<int:pk>', views.StartupDetailView.as_view(), name='detail-startup'),
    # position path
    path('jobs/', views.client_jobs_index, name='client-jobs-index'),
    path('jobs/positions/<int:pk>', views.JobPositionDetailView.as_view(), name='detail-job-position'),
    path('jobs/positions/list', views.JobPositionListView.as_view(), name='list-job-position'),
    path('jobs/applications/list', views.JobApplicationListView.as_view(), name='list-job-application'),
]
