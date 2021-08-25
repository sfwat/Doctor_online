from django.urls import path

from .views import DoctorRegistration, PatientRegistration, UserLogin, CategoryList, CategoryDetails,\
        ClinicAdding, DoctorClinics, PatientClinics, ClinicReservation
urlpatterns = [
        path("doctor_register", DoctorRegistration.as_view()),
        path("patient_register", PatientRegistration.as_view()),
        path("login", UserLogin.as_view()),
        path("category", CategoryList.as_view()),
        path("category/<int:pk>", CategoryDetails.as_view()),
        path("clinicAdding", ClinicAdding.as_view()),
        path("doctor/<int:pk>", DoctorClinics.as_view()),
        path("patient", PatientClinics.as_view()),
        path("clinic/<int:pk>", ClinicReservation.as_view())
]
