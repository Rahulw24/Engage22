from django.urls import path,include
from .views import *

urlpatterns = [
    # landing page
    path('',index,name='index'),

    #login URLs
    path('login/',login,name='login'),
    path('login_scan/',login_scan,name='login_scan'),
    
    # employee  URLs
    path("employee_details/",employee_details, name="employee_details"),
    
    #manager URLs
    path('manager/', manager, name= 'manager'),
    path('clear_history/',clear_history,name='clear_history'),
    path('reset/',reset,name='reset'),
    path('search_name/',search_name,name='search_name'),
    path('search_date/',search_date,name='search_date'),
    path('scan/',scan,name='scan'),
    path('stop_scan/',stop_scan,name='stop_scan'),
    path('details/', details, name= 'details'),
    
    # Profile URLs
    path('profiles/', profiles, name= 'profiles'),
    path('add_profile/',add_profile,name='add_profile'),
    path('edit_profile/<int:id>/',edit_profile,name='edit_profile'),
    path('delete_profile/<int:id>/',delete_profile,name='delete_profile'),
    
    path('ajax/', ajax, name= 'ajax'),

]
