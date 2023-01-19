from django.shortcuts import render
from django.http import HttpResponse
from .forms import Insert_automation_data
from django.views import generic
from .models import automation_db

# Create your views here.
def home(request):
    return render(request, "Index.html", context={})

class index(generic.ListView):
    model = automation_db
    template_name = 'Index.html'

    def render_to_response(self, context):
        no_reg_script_auto = automation_db.objects.raw("select NO_OF_REGSCRIPTS_AUTOMATED from automation_db")
        sum_nr = 0
        for nr in no_reg_script_auto:
            sum_nr = sum_nr + int(nr)

        print(sum_nr)

        return render(request, 'Index.html', context={'sum_nr': sum_nr})



class Insert_automation_data_view(generic.CreateView):
    form_class = Insert_automation_data
    model = automation_db
    template_name = 'Insert_automation_data.html'
    success_url = '/list/createdata'

class table_automation_view(generic.ListView):
    model = automation_db
    template_name = 'table_automation.html'

