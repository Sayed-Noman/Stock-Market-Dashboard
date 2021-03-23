from django.urls import path
from home import views
from home.dash_apps.finished_apps import examples
urlpatterns = [
    path('',views.dashboard,name='dashboard')
]
