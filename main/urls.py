from django.urls import path
from . import views as v

app_name = "main"

urlpatterns = [
    path('', v.home, name='home'),
    path('logout/', v.logout, name='logout'),
    path('most-requested/', v.most_requested_services, name='most_requested_services')
]
