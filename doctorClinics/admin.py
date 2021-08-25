from django.contrib import admin
from doctorClinics.models import Category, Doctor, Patient, Clinic
# Register your models here.


admin.site.register(Category)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Clinic)
