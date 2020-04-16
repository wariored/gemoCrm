from django.urls import path
from . import views

app_name = "sales"

urlpatterns = [
    # contact
    path('index', views.ContactListView.as_view(), name='list-contact'),
    path('contact-detail/<int:pk>', views.ContactDetailView.as_view(), name='detail-contact'),
    path('contact-create', views.ContactCreateView.as_view(), name='create-contact'),
    path('contact-update/<int:pk>', views.ContactUpdateView.as_view(), name='update-contact'),
    # deal
    path('deal-detail/<int:pk>', views.DealDetailView.as_view(), name='detail-deal'),
    path('deal-create', views.DealCreateView.as_view(), name='create-deal'),
    path('deal-update/<int:pk>', views.DealUpdateView.as_view(), name='update-deal'),
    path('deal-list', views.DealListView.as_view(), name='list-deal'),
]
