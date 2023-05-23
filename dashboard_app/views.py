from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .forms import Insert_automation_data
from django.views import generic
from .models import automation_db
from django.db.models import Avg, Sum
from django.urls import reverse
import pandas as pd
from django.db import transaction

# Create your views here.
def home(request):
    return redirect('Dashboard')

class index(generic.ListView):
    model = automation_db
    template_name = 'Index.html'

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
        form = Insert_automation_data(request.POST)
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
