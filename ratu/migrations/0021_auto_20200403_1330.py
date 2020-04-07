# Generated by Django 2.0.9 on 2020-04-03 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ratu', '0020_delete_rfop'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rfop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=300, null=True)),
                ('kved', models.CharField(max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='State_Rfop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='rfop',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ratu.State_Rfop'),
        ),
    ]