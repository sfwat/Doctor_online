from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Clinic, Doctor, Patient
from .serializer import DoctorRegistrationSerializer, PatientRegistrationSerializer, UserLoginSerializer, \
    CategorySerializer, CategoryDetailsSerializer, ClinicSerializer, DoctorSerializer, PatientSerializer


class DoctorRegistration(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = DoctorRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PatientRegistration(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = PatientRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLogin(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryList(APIView,):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetails(APIView,):

    def get_object(self, pk):
        try:
            category = Category.objects.get(pk=pk)
            return category
        except Category.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        category = self.get_object(pk)
        if isinstance(category, HttpResponse):
            return category
        serializer = CategoryDetailsSerializer(category)
        return Response(serializer.data)


class DoctorClinics(APIView,):

    def get_object(self, pk):
        doctor = Doctor.objects.get(pk=pk)
        return doctor

    def get(self, request, pk):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)


class ClinicAdding(APIView,):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (api_settings.DEFAULT_AUTHENTICATION_CLASSES[0],)

    def post(self, request):

        request.data["doctor"] = request.user
        serializer = ClinicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientClinics(APIView,):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (api_settings.DEFAULT_AUTHENTICATION_CLASSES[1],)

    def get_object(self, pk):
        patient = Patient.objects.get(pk=pk)
        return patient

    def get(self, request):
        patient = self.get_object(request.user.id)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)


class ClinicReservation(APIView,):

    authentication_classes = (api_settings.DEFAULT_AUTHENTICATION_CLASSES[1],)
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            clinic = Clinic.objects.get(pk=pk)
            return clinic
        except Clinic.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self,request, pk):
        clinic = self.get_object(pk)
        if isinstance(clinic,HttpResponse):
            return clinic
        serializer = ClinicSerializer(clinic)
        return Response(serializer.data)

    def put(self, request, pk):
        clinic = self.get_object(pk)
        if isinstance(clinic,HttpResponse):
            return clinic
        try:
            clinic.patient = request.user
            clinic.reserved = True
            clinic.save()
            serializer = ClinicSerializer(clinic)
            return Response(serializer.data)
        return HttpResponse(status=status.HTTP_500_INTERNAL_SERVER_ERROR
)



