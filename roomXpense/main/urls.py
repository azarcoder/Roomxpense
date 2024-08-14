from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login', views.login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('signup/', views.sign_up, name='signup'),
    path('newroom/', views.newroom, name='newroom'),
    path('add_person', views.add_person, name='add_person'),
    path('view_members/<int:room_id>', views.view_members, name = 'view_members'),
    path('transactions/<int:room_id>', views.transactions, name='transactions'),
    path('settle/<int:room_id>', views.settle, name='settle')
]