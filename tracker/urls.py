from django.urls import path
from . import views

urlpatterns=[
    path('',views.dashboard,name='dashboard'),
    
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout_view'), 
    
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-category/', views.add_category, name='add_category'),
    path('remove-expense/<int:expense_id>',views.remove_expense,name='remove-expense'),
    path('pie-chart/', views.pie_chart_view, name='pie-chart'),

    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
]