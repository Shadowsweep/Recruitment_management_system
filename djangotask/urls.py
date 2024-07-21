"""
URL configuration for djangotask project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path,re_path
from Registerapp import views
from django.conf.urls.static import static 

urlpatterns = [
    path('', views.homepage),
    path('create_profile/', views.create_profile, name='create_profile'),
    path('create_user/', views.create_user, name='create_user'),
    path('list/', views.profile_list,name='profile_list'),
    path('delete/<int:profile_id>/', views.delete_profile, name='delete_profile'),
    path('edit/<int:profile_id>/', views.edit_profile, name='edit_profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('logout/', views.log_out, name='logout'),
    path('blog_create/', views.blog_create, name='blog_create'),
    path('create_blog_post/', views.create_blog_post, name='create_blog_post'),
    path('draft_blog/', views.draft_blog, name='draft_blog'),
    path('edit-blog/<int:blog_id>/', views.edit_blog, name='edit_blog'),
    path('delete-blog/<int:blog_id>/', views.delete_blog, name='delete_blog'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('check-availability/', views.check_availability, name='check_availability'),
    path('success_form/', views.success_form, name='success_form'),
    path('add_student/', views.add_student, name='add_student'),
    path('signup_student/', views.signup_student, name='signup_student'),
    path('save_student/', views.save_student, name='save_student'),
    # path('admin_signup/', views.signup_admin, name='admin_signup'),
    path('signup_admin/', views.signup_admin, name='signup_admin'),
    # path('admin_dashboard/<str:admin_id>/', views.admin_dashboard, name='admin_dashboard'),
    path('home', views.homepage, name='home'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('login/', views.login_view, name='login'),
    path('search-student-profile/', views.search_student_profile, name='search_student_profile'),
    path('update-student-profile/', views.update_student_profile, name='update_student_profile'),
    path('edit_student_profile/', views.edit_student_profile, name='edit_student_profile'),
    # path('register/', views.register_user, name='register_user'),
    path('create_placement_drive/', views.create_placement_drive, name='create_placement_drive'),
    path('create_placement/', views.placementdrive_page, name='create_placement'),
    path('edit_placement_drive/<int:id>/', views.edit_placement_drive, name='edit_placement_drive'),
    path('delete_placement_drive/<int:id>/', views.delete_placement_drive, name='delete_placement_drive'),
    # path('edit_admin_page/<int:admin_id>/', views.edit_admin_page, name='edit_admin_page'),
    # path('edit_admin/<int:admin_id>/', views.edit_admin, name='edit_admin'),
    #  re_path(r'^api/uploadjson',file_view.upload_insight),
]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
