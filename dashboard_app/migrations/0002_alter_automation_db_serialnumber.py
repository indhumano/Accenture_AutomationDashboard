# Generated by Django 4.0.6 on 2022-12-21 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='automation_db',
            name='serialnumber',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]