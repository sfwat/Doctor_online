import jwt
import time
from django.db import models
from django.conf import settings

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from datetime import datetime, timedelta
from enumchoicefield import ChoiceEnum, EnumChoiceField


# Create your models here.


class ClinicCategory(ChoiceEnum):
    Dermatology = "الجلدية-Dermatology"
    Cardiology = "القلب-Cardiology"
    Ophthalmology = "Ophthalmology-العيون"
    Nutrition = "Nutrition-تغذية"
    Allergy = "Allergy-الحساسية"


class Category(models.Model):

    title = EnumChoiceField(enum_class=ClinicCategory)

    def __str__(self):
        return self.title.verbose_name


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class DoctorManager(BaseUserManager):

    def create_doctor(self, username, email, category, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')
        doctor = Doctor(username=username, email=self.normalize_email(email), category=category)
        doctor.set_password(password)
        doctor.save()
        return doctor


class PatientManager(BaseUserManager):

    def create_patient(self, username, email, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')
        patient = Patient(username=username,
                          email=self.normalize_email(email))
        patient.set_password(password)
        patient.save()
        return patient


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # a admin user; non super-user
    is_superuser = models.BooleanField(default=False)  # a superuser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = UserManager()

    @property
    def token(self):
        dt = datetime.now() + timedelta(days=1)
        token = jwt.encode({
            'id': self.id,
            'exp': int(time.mktime(dt.timetuple()))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token

    def __str__(self):
        return self.email


class Doctor(CustomUser, PermissionsMixin):

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="doctors")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'category']

    objects = DoctorManager()

    def __str__(self):
        return f" name: {self.username} id:{self.id}"


class Patient(CustomUser, PermissionsMixin):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = PatientManager()

    def __str__(self):
        return self.username


class Clinic(models.Model):
    name = models.CharField(max_length=20)
    price = models.PositiveIntegerField()
    cancelled = models.BooleanField(default=False)
    reserved = models.BooleanField(default=False)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='clinics')
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='clinics')

    def __str__(self):
        return f"clinic_id:{self.id}, name:{self.name}, date:{self.date} start_at: {self.start_time} ends_at:{self.end_time}" \
               f" doctor: {self.doctor.username}, patient: {self.patient.username if self.patient else '-----'}"

