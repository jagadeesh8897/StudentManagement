"""
URL configuration for StudentManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('',views.home,name='home'),
    path('login/',views.loginn,name='login'),
    path('loginadmin/',views.loginAdmin,name='loginadmin'),
    path('register/',views.register,name='register'),
    path('registeradmin/',views.registerAdmin,name='registeradmin'),
    path('homee/',views.homee,name='homee'),
    path('base/',views.base,name='base'),
    path('studentm/',views.studentm,name='studentm'),
    path('submit/',views.newStudent,name='newstudent'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('edit/<int:id>',views.edit,name='edit'),
    path('update/<int:id>',views.update,name='update'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('results/', views.results, name='results'),
    path('selecttype/',views.selectType,name='selecttype'),
    path('studentpage/',views.studentpage,name='studentpage'),
    path('studentProfile/',views.studentProfile,name='studentprofile'),
path('update_marks/<int:student_id>/', views.update_marks, name='update_marks'),
path('view_marks/<int:student_id>/', views.view_marks, name='view_marks'),
path('view_result/', views.student_result_view, name='student_result'),
    path('feedback/', views.submit_feedback, name='submit_feedback'),
    path('admin-feedbacks/', views.view_feedbacks, name='view_feedbacks'),
path('leave/', views.submit_leave, name='leave'),
    path('adminleave/', views.view_leave, name='adminleave'),
# Use ISO-formatted datetime as a URL-safe string (you'll pass it via GET or POST)
path('approve-leave/<str:submitted_at>/', views.approve_leave_by_time, name='approve_leave_by_time'),


]
