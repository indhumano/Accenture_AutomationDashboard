from django.contrib import admin
from django.urls import path, include
from .views import home, Insert_automation_data_view, table_automation_view, index, upload_excel
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #path('', home, name='Index'),
    path('', index.as_view(), name='Index'),
    path('list/createdata', Insert_automation_data_view.as_view(), name='Insert_automation_data'),
    path('list', table_automation_view.as_view(), name='table_automation'),
    path('upload_excel', upload_excel, name='upload_excel'),

]
