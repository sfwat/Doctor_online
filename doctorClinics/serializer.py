from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Doctor, Patient, Category, Clinic


class DoctorRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Doctor
        fields = '__all__'


    def create(self, validated_data):
        return Doctor.objects.create_doctor(**validated_data)


class PatientRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'

    def create(self, validated_data):
        return Patient.objects.create_patient(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)
        print(email, password)
        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)
        print(user)
        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            userObj = Doctor.objects.get(email=user.email)
        except Doctor.DoesNotExist:
            userObj = None

        try:
            if userObj is None:
                userObj = Patient.objects.get(email=user.email)
        except Patient.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )

            # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'token': user.token
        }


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("__all__")


class CategoryDetailsSerializer(serializers.ModelSerializer):
    doctors = serializers.StringRelatedField(many=True)
    class Meta:
        model = Category
        fields = ("__all__")


class DoctorSerializer(serializers.ModelSerializer):
    clinics = serializers.StringRelatedField(many=True)

    class Meta:
        model = Doctor
        fields = ["username", "clinics"]


class PatientSerializer(serializers.ModelSerializer):
    clinics = serializers.StringRelatedField(many=True)

    class Meta:
        model = Patient
        fields = ["username", "clinics"]


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = ("__all__")

