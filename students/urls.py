from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('add/', views.add_student, name='add_student'),
    path('<int:pk>/', views.student_detail, name='student_detail'),
    path('<int:pk>/edit/', views.edit_student, name='edit_student'),
    path('<int:pk>/delete/', views.delete_student, name='delete_student'),
    path('group/<str:group_name>/', views.group_detail, name='group_detail'),
]