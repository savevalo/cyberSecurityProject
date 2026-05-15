from django.urls import path

from .views import index, transferView, accountView, registerView

urlpatterns = [
    path('', index, name='home'),
    path('transfer/', transferView, name='transfer'),
    path('account/<int:id>/', accountView, name='account'),
    path('register/', registerView, name='register'),
    
]