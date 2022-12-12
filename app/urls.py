from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.do_login, name='login'),
    path('signup_view', views.signup_view, name='signup_view'),
    path('login_view', views.login_view, name='login_view'),
    path('logout', views.logout_view, name='logout'),
    path('become_tenant', views.become_tenant, name='become_tenant'),
    path('become_landlord', views.become_landlord, name='become_landlord'),
    path('make_room', views.make_room, name='make_room'),
    path('clear_room',views.clear_room, name='clear_room'),
    path('manage_rooms', views.manage_rooms, name='manage_rooms'),
    path('requested', views.requested, name='requested'),
    path('my_requests', views.my_requests, name='my_requests'),
    path('request_room', views.request_room, name='request_room'),
    path("view_rooms", views.view_rooms, name= 'view_rooms'),

    
]