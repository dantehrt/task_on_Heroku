from django.urls import path

from . import views

app_name = 'mturk'
urlpatterns = [
    path('<str:worker_id>/<str:assignment_id>/<str:task_condition>/', views.index, name='index'),
    path('<str:worker_id>/<str:assignment_id>/<str:task_condition>/<int:task_order>', views.task, name='task'),
    path('<str:worker_id>/<str:assignment_id>/<str:task_condition>/<int:task_order>/submit', views.submit, name='submit'),
    path('<str:worker_id>/<str:assignment_id>/<str:task_condition>/results', views.results, name='results'),
    path('<str:worker_id>/<str:assignment_id>/thanks', views.thanks, name='thanks'),
    path('<str:worker_id>/is_there', views.is_there, name='is_there'),
]