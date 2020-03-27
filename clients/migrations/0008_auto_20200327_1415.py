# Generated by Django 3.0 on 2020-03-27 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_auto_20200327_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='startup',
            name='kind',
            field=models.CharField(blank=True, choices=[('L', 'LEAD'), ('HL', 'HOT LEAD'), ('C', 'CLIENT')], max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='positions',
            field=models.ManyToManyField(blank=True, related_name='job_applications', to='clients.JobPosition'),
        ),
    ]
