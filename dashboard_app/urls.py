from django.contrib import admin
from django.urls import path, include
from .views import home, Insert_automation_data_view, table_automation_view, index, upload_excel, log_out, get_graph_data
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from .views import LoginView

urlpatterns = [
    path('', RedirectView.as_view(url='/login/')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', log_out, name='logout'),
    path('get_graph_data/', get_graph_data, name='get_graph_data'),
    path('', home, name='Home'),
    path('dashboard/', login_required(index.as_view()), name='Dashboard'),
    path('list/createdata/', Insert_automation_data_view, name='Insert_automation_data'),
    # path('list/', table_automation_view.as_view(), name='table_automation'),
    path('upload_excel/', upload_excel, name='upload_excel'),

]
