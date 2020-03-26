from django.urls import path

from . import views

app_name = 'clients'
urlpatterns = [
    path('', views.client_index, name='client-index'),
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
]
