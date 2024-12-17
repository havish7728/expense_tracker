from django.urls import path
from . import views

urlpatterns=[
    path('',views.dashboard,name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-category/', views.add_category, name='add_category'),
    path('remove-expense/<int:expense_id>',views.remove_expense,name='remove-expense'),

    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout_view'), 
]