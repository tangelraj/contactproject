from django.urls import path
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact_manual, name='manual'),       # manual form at /
    path('model/', views.contact_model, name='model'),   # ModelForm at /model/
    path('success/', views.success, name='success'),
]
