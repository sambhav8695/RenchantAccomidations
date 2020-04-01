from django.urls import path
from . import views

urlpatterns = [
    path('home', views.Index.as_view(), name='index'),
    path('contact', views.Contact.as_view(), name='contact'),
    path('details/<int:pk>', views.details, name="details"),
    path('schedule', views.schedule_property, name="schedule_property"),
    path('', views.about, name='about'),
    path('add', views.AddProperty.as_view(), name="add_property"),
    path('list', views.PropertyListOwner.as_view(), name="property_list"),
    path('auth_property_details/<int:pk>', views.DetailProperty.as_view(), name='auth_property_details'),
    path('payment', views.Payment.as_view(), name='payment'),
]
