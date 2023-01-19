from django.db import models

# Create your models here.
class automation_db(models.Model):
    serialnumber = models.IntegerField(primary_key=True, unique=True)
    month = models.CharField(max_length=15)
    year = models.CharField(max_length=10)
    portfolio = models.CharField(max_length=10)
    AIT_Number = models.IntegerField()
    application_name = models.CharField(max_length=30)
    could_noncloud = models.CharField(max_length=10)
    Automation_status = models.CharField(max_length=15)
    automation_tool = models.CharField(max_length=20)
    in_sprint = models.CharField(max_length=10)
    litmus_onboarding = models.CharField(max_length=10)
    no_of_overall_regression_scripts = models.CharField(max_length=20)
    no_of_inscope_reg_scripts = models.CharField(max_length=20)
    no_of_regscripts_automated = models.CharField(max_length=20)
    percentage_automation_complete = models.CharField(max_length=20)
    percentage_application_penetration = models.CharField(max_length=20)
    time_to_manuallyexecute = models.CharField(max_length=20)
    no_of_release = models.CharField(max_length=10)
    monthly_manual_executiontime = models.CharField(max_length=20)
    monthly_effort_spent_on_dev_automation = models.CharField(max_length=20)
    time_to_execute_1automatedtestcase = models.CharField(max_length=20)
    mothly_automate_executiontime = models.CharField(max_length=20)
    monthly_effort_spentin_maintaining_automation = models.CharField(max_length=20)
    monthly_effort_takes_toexecute_regscript = models.CharField(max_length=20)
    hours_saved_monthly = models.CharField(max_length=20)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.serialnumber) + " " + self.portfolio + " " + str(self.AIT_Number)