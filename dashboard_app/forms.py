from django import forms
from .models import automation_db

class Insert_automation_data(forms.ModelForm):
    class Meta:
        model = automation_db
        fields = "__all__"
        #fields = ['student_id','name','email','phone_number','teacher']