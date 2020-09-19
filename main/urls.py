from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('dashboard', views.dashboard),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('jobs/new', views.newjob),
    path('createjob', views.createjob),
    path('jobs/<int:job_id>', views.showjob),
    path('jobs/edit/<int:job_id>', views.editjob),
    path('updatejob', views.updatejob),
    path('deletejob', views.deletejob),
    path('addtomyjobs', views.addtomyjobs),
    path('dashboard/<int:job_id>', views.changelist),
]