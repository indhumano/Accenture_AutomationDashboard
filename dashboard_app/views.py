from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from .forms import Insert_automation_data
from django.views import generic
from .models import automation_db
from django.db.models import Avg, Sum
from django.urls import reverse
import pandas as pd
from django.db import transaction
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.template import loader
from django.http import HttpResponse
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def home(request):
    return redirect('Dashboard')


class LoginView(View):
    template_name = 'dashboard-login.html'

    def get(self, request):
        template = loader.get_template(self.template_name)
        context = {'redirection_url': request.GET.get('next')}
        return HttpResponse(template.render(context, request))

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            redirection_url = request.POST.get('redirection_url')
            redirection_url = None if redirection_url == 'None' else redirection_url
            if redirection_url is not None:
                return HttpResponseRedirect(redirection_url)
            else:
                return HttpResponseRedirect(reverse('Dashboard'))
        else:
            return self.get(request)


class index(generic.ListView):
    model = automation_db
    template_name = 'Index.html'
    login_url = '/login/'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(index, self).get_context_data(**kwargs)
        context['no_of_overall_regression_scripts'] = \
        automation_db.objects.aggregate(no_of_overall_regression_scripts=Sum('no_of_overall_regression_scripts'))[
            'no_of_overall_regression_scripts']  # 1
        context['no_of_inscope_reg_scripts'] = \
        automation_db.objects.aggregate(no_of_inscope_reg_scripts=Sum('no_of_inscope_reg_scripts'))[
            'no_of_inscope_reg_scripts']  # 2
        context['no_of_regscripts_automated'] = \
        automation_db.objects.aggregate(no_of_regscripts_automated=Sum('no_of_regscripts_automated'))[
            'no_of_regscripts_automated']  # 3
        context['percentage_automation_complete_average'] = \
        automation_db.objects.aggregate(percentage_automation_complete_average=Avg('percentage_automation_complete'))[
            'percentage_automation_complete_average']  # 4
        context['percentage_application_penetration_average'] = automation_db.objects.aggregate(
            percentage_application_penetration_average=Avg('percentage_application_penetration'))[
            'percentage_application_penetration_average']  # 5
        return context

def Insert_automation_data_view(request):
    # form_class = Insert_automation_data
    # model = automation_db
    # template_name = 'Insert_automation_data.html'
    # success_url = '/list/createdata'
    if "GET" == request.method:
        return render(request, 'Insert_automation_data.html')
    else:
        updated_request = request.POST.copy()
        serial_number = automation_db.objects.latest('pk').pk
        serial_number += 1
        no_of_regscripts_automated = int(updated_request.get('no_of_regscripts_automated'))
        no_of_overall_regression_scripts = int(updated_request.get('no_of_overall_regression_scripts'))
        no_of_inscope_reg_scripts = int(updated_request.get('no_of_inscope_reg_scripts'))
        percentage_automation_complete = str(round((no_of_regscripts_automated/no_of_overall_regression_scripts)*100))
        percentage_application_penetration = str(round((no_of_regscripts_automated/no_of_inscope_reg_scripts)*100))
        updated_request.update({'percentage_automation_complete': percentage_automation_complete})
        updated_request.update({'percentage_application_penetration': percentage_application_penetration})
        updated_request.update({'serialnumber': serial_number})
        form = Insert_automation_data(updated_request)
        if form.is_valid():
            new_automation_entry = form.save()
            return render(request, 'Insert_automation_data.html', {'message': 'New Entry Done successfully'})
        else:
            print(form.errors)
            return render(request, 'Insert_automation_data.html', {'message': 'Error while doing entry'})

class table_automation_view(generic.ListView):
    model = automation_db
    template_name = 'table_automation.html'

def upload_excel(request):
    if "GET" == request.method:
        return render(request, 'dashboard_app/Index.html', {})
    else:
        excel_file = request.FILES["excel_data"]
        columns_with_data = list(range(26))
        file_df = pd.read_excel(excel_file, sheet_name='Sheet1', usecols=columns_with_data)

        for index, row in file_df.iterrows():
            serialnumber = row['SERIALNUMBER']
            month = row['MONTH']
            year = row['YEAR']
            portfolio = row['PORTFOLIO']
            AIT_Number = row['AIT_NUMBER']
            application_name = row['APPLICATION_NAME']
            could_noncloud = row['COULD_NONCLOUD']
            Automation_status = row['AUTOMATION_STATUS']
            automation_tool = row['AUTOMATION_TOOL']
            in_sprint = row['IN_SPRINT']
            litmus_onboarding = row['LITMUS_ONBOARDING']
            no_of_overall_regression_scripts = row['NO_OF_OVERALL_REGRESSION_SCRIPTS']
            no_of_inscope_reg_scripts = row['NO_OF_INSCOPE_REG_SCRIPTS']
            no_of_regscripts_automated = row['NO_OF_REGSCRIPTS_AUTOMATED']
            percentage_automation_complete = row['PERCENTAGE_AUTOMATION_COMPLETE']
            percentage_application_penetration = row['PERCENTAGE_APPLICATION_PENETRATION']
            time_to_manuallyexecute = row['TIME_TO_MANUALLYEXECUTE']
            no_of_release = row['NO_OF_RELEASE']
            monthly_manual_executiontime = row['MONTHLY_MANUAL_EXECUTIONTIME']
            monthly_effort_spent_on_dev_automation = row['MONTHLY_EFFORT_SPENT_ON_DEV_AUTOMATION']
            time_to_execute_1automatedtestcase = row['TIME_TO_EXECUTE_1AUTOMATEDTESTCASE']
            mothly_automate_executiontime = row['MOTHLY_AUTOMATE_EXECUTIONTIME']
            monthly_effort_spentin_maintaining_automation = row['MONTHLY_EFFORT_SPENTIN_MAINTAINING_AUTOMATION']
            monthly_effort_takes_toexecute_regscript = row['MONTHLY_EFFORT_TAKES_TOEXECUTE_REGSCRIPT']
            hours_saved_monthly = row['HOURS_SAVED_MONTHLY']
            comments = row['COMMENTS']

            with transaction.atomic():
                object = automation_db(serialnumber=serialnumber, month=month, year=year, portfolio=portfolio, AIT_Number=AIT_Number,
                              application_name=application_name,
                              could_noncloud=could_noncloud, Automation_status=Automation_status,
                              automation_tool=automation_tool, in_sprint=in_sprint,
                              litmus_onboarding=litmus_onboarding,
                              no_of_overall_regression_scripts=no_of_overall_regression_scripts,
                              no_of_inscope_reg_scripts=no_of_inscope_reg_scripts,
                              no_of_regscripts_automated=no_of_regscripts_automated,
                              percentage_automation_complete=percentage_automation_complete,
                              percentage_application_penetration=percentage_application_penetration,
                              time_to_manuallyexecute=time_to_manuallyexecute,
                              no_of_release=no_of_release,
                              monthly_manual_executiontime=monthly_manual_executiontime,
                              monthly_effort_spent_on_dev_automation=monthly_effort_spent_on_dev_automation,
                              time_to_execute_1automatedtestcase=time_to_execute_1automatedtestcase,
                              mothly_automate_executiontime=mothly_automate_executiontime,
                              monthly_effort_spentin_maintaining_automation=monthly_effort_spentin_maintaining_automation,
                              monthly_effort_takes_toexecute_regscript=monthly_effort_takes_toexecute_regscript,
                              hours_saved_monthly=hours_saved_monthly,
                              comments=comments)
                object.save()
                print(object.serialnumber)

        return HttpResponseRedirect(reverse('Index'))

def log_out(request):
    logout(request)
    return redirect('login')

def get_graph_data(request):
    current_year = datetime.now().date().strftime("%Y")
    year = request.GET.get("TAyear", current_year)
    reg_test_cases = automation_db.objects.filter(year=year).values('month').annotate(sum=Sum('no_of_overall_regression_scripts'))
    reg_automatable = automation_db.objects.filter(year=year).values('month').annotate(sum=Sum('no_of_inscope_reg_scripts'))
    reg_automated = automation_db.objects.filter(year=year).values('month').annotate(sum=Sum('no_of_regscripts_automated'))

    test_cases = []
    automatable = []
    automated = []
    for t in reg_test_cases:
        test_cases.append(t)

    for amble in reg_automatable:
        automatable.append(amble)

    for amted in reg_automated:
        automated.append(amted)

    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    m_order = {key: i for i, key in enumerate(month_order)}
    test_cases_ordered = sorted(test_cases, key=lambda d: m_order[d['month']])
    automatable_ordered = sorted(automatable, key=lambda d: m_order[d['month']])
    automated_ordered = sorted(automated, key=lambda d: m_order[d['month']])

    reg_test_cases_data = [tco['sum'] for tco in test_cases_ordered]
    reg_automatable_data = [ao['sum'] for ao in automatable_ordered]
    reg_automated_data = [ato['sum'] for ato in automated_ordered]

    series = []
    reg_test_cases_dict = {}
    reg_test_cases_dict['name'] = "Regression Test Cases"
    reg_test_cases_dict['data'] = reg_test_cases_data
    series.append(reg_test_cases_dict)

    reg_automatable_dict = {}
    reg_automatable_dict['name'] = "Regression Automatable"
    reg_automatable_dict['data'] = reg_automatable_data
    series.append(reg_automatable_dict)

    reg_automated_dict = {}
    reg_automated_dict['name'] = "Regression Automated"
    reg_automated_dict['data'] = reg_automated_data
    series.append(reg_automated_dict)

    response = series
    return JsonResponse(response, safe=False)
