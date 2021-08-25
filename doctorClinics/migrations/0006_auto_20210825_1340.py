# Generated by Django 3.2.6 on 2021-08-25 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctorClinics', '0005_alter_clinic_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clinics', to='doctorClinics.patient'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctors', to='doctorClinics.category'),
        ),
    ]
