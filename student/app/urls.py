from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('students/', views.students, name='students'), 
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_students, name='add_students'),  
    path('feesrecord/', views.feesrecord, name='feesrecord'),
    path('excel/', views.excel, name='excel'),
    path('update/<int:student_id>/', views.update_student, name='update_student'),

    # path('delete/<int:id>/', views.delete_student, name='delete_student'),

]

