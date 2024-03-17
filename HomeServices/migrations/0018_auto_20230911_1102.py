# Generated by Django 3.0 on 2023-09-11 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeServices', '0017_remove_service_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='date',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='appointement_dates',
            field=models.ManyToManyField(to='HomeServices.date'),
        ),
    ]