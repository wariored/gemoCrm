# Generated by Django 3.0 on 2020-03-31 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_auto_20200328_2303'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('from_type', models.CharField(choices=[('H', 'Hacker'), ('S', 'Startup'), ('T', 'Team Member')], max_length=30)),
                ('to_type', models.CharField(choices=[('H', 'Hacker'), ('S', 'Startup'), ('T', 'Team Member')], max_length=30)),
                ('from_email', models.EmailField(max_length=254)),
                ('to_email', models.EmailField(max_length=254)),
            ],
        ),
    ]