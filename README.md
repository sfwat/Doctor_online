# Doctor_online
A rest api  project for a virtual clinic using Django restframework
## content.
*  How to run app
*  Api Documentation

How to run app
=====================================
1. Clone git repo https://github.com/sfwat/Doctor_online.git
2. Make sure you are on master branch **$git checkout master**
3. Create and activate Virtual environment **$virtualenv venv**    **$source/venv/bin/activate**
4. Move to Doctor Online dir and install packages from requirments file **$ pip install -r requirments.txt**
5. run migration command  **$python manage.py makemigrations**  **$python manage.py migrate**
6. run the server **python manage.py runserver**

Api Documentation
======================================

### There are two types of registration first Doctor registration and second Patient registration

### But first let's talk about authorization in this project where some endpoint use no auth and others need credentials

## For example Listing all categories use no auth which list all the clinic categories

## Category  [/category] 


### CategoryList [GET]

+ Response 200 ok (application/json)
  + body

            [
                {
                    "id": 1,
                    "title": "Dermatology"
                },
                {
                    "id": 2,
                    "title": "Cardiology"
                },
                {
                    "id": 4,
                    "title": "Ophthalmology"
                },
                {
                    "id": 5,
                    "title": "Nutrition"
                },
                {
                    "id": 6,
                    "title": "Allergy"
                }
            ]
  
### Be sure to add all the categories you want before start testing some are added ClinicCategory class
### you can update it with more or just use the existing ones just create a super user 
### **python manage.py createsuperuser**
### login to Admin site and add some categories

## Back to how to register now we have some categories and Doctors are ready to register

## Register  [/doctor_register] 


### Doctor register [POST]

+ Body
    
           {
               "username": "test user",
               "password": "testpassword",
               "email": "test@test.com",
               "category": 1
           }

## the category value is the id of any existing category

+ 201 created (application/json)

    + Body
    
            {
                "id": 6,
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NiwiZXhwIjoxNjMwMDA1MTgyfQ.uvaoHHDrp5L6j7h4WjO4pJIVUDYtYUgiSSn_LN2kjdc",
                "last_login": null,
                "username": "test user",
                "email": "test@test.com",
                "is_active": true,
                "is_staff": false,
                "is_superuser": false,
                "category": 1,
                "groups": [],
                "user_permissions": []
            }   

## Patient register is not so different from doctor  the only difference is the category

## Register  [/patient_register] 


### Patient register [POST]

+ Body
    
           {
               "username": "test patient",
               "password": "testpassword",
               "email": "test@test.io"
           }
+ 201 created (application/json)

    + Body
    
            {
                "id": 7,
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NiwiZXhwIjoxNjMwMDA1MTgyfQ.uvaoHHDrp5L6j7h4WjO4pJIVUDYtYUgiSSn_LN2kjdc",
                "last_login": null,
                "username": "test user",
                "email": "test@test.com",
                "is_active": true,
                "is_staff": false,
                "is_superuser": false
                "groups": [],
                "user_permissions": []
            }   

### All the previous requests didn't use any type of auth but now let's check some endpoints that need credentials

## User login [/login]

## logging in [POST]

## login work with both type of user fine all you need to provide is a valid email and password
+ Request
  + Body
    
           {
               "password": "testpassword",
               "email": "test@test.io"
           }
+ Response 200 ok (application/json)

   + Body
              
            {
              "email": "pateinttest@test.te",
              "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NSwiZXhwIjoxNjMwMDA1Njg2fQ.sNu9bK6QhAF4oLtC2WlicwXqWpF8Kr6KhM6o9nKeY68"
            }

### You need to save the user token that returns, so you can use it later

### Just like Listing Categories listing a single Category details need no auth

## Category Details  [/category/<int:pk>] 


### single Category details [GET]

+ Response 200 ok (application/json)

   + Body
              
            {
               "id": 1,
               "doctors": [
                 " name: mohamed ahmed id:1",
                 " name: test user id:6"
               ],
               "title": "Dermatology"
            }

### the details are all doctors under the same category

## Now it's time for our Doctor to add some clinics
### This will be the frist endpoint we need to use the auth token with it 

## Add Clinic [POST]
### ClinicAdding [/clinicAdding]

+ Request
  + header     ```Authorization: Token DoctorAuthToken```

+ Body 
     ```
              {
                "name":"test clinic",
                "date": "2021-10-01",
                "start_time": "14:00",
                "end_time": "15:00",
                "price": 100
              }
     ```
  
+ Response 201 created (application/json)
  + Body
    ``` 
    {
        "id": 4,
        "name": "test clinic",
        "price": 100,
        "cancelled": false,
        "reserved": false,
        "date": "2021-10-01",
        "start_time": "14:00:00",
        "end_time": "15:00:00",
        "doctor": 6,
        "patient": null
    }
    ```

### If this request is sent by a patient it will be refused                      
### Now let's reserve a clinic for a patient

## Reserve Clinic [PUT]
### ClinicReservation [clinic/<int:pk>]

+ Request
  + header     ```Authorization: Token PatientAuthToken```
  
+ Response 200 ok (application/json)
  + Body
    ``` 
    {   
        "id": 4,
        "name": "test clinic",
        "price": 100,
        "cancelled": false,
        "reserved": true,
        "date": "2021-10-01",
        "start_time": "14:00:00",
        "end_time": "15:00:00",
        "doctor": 6,
        "patient": 5
    }
    ```
    
### If this request is sent by a doctor it will be refused
    
### Finally let's show clinics for both doctors and patients


## Doctors Clinic [GET]
### Doctors ClinicList [doctor/<int:pk>]

+ Request
  
+ Response 200 ok (application/json)
  + Body
    ``` 
    {
    "username": "mohamed ahmed",
    "clinics": [
        "clinic_id:1, name:test clinic, date:2021-08-02 start_at: 20:00:00 ends_at:20:30:00 doctor: mohamed ahmed, patient: test",
        "clinic_id:2, name:test clinic, date:2021-12-12 start_at: 12:30:00 ends_at:13:00:00 doctor: mohamed ahmed, patient: not yet"
    ]
}
    ```
## Patient Clinic [GET]
### Patient ClinicList [patient]

+ Request
  + header     ```Authorization: Token PateintAuthToken```

+ Response 200 ok (application/json)
  + Body
    ``` 
    {
    "username": "patient",
    "clinics": [
        "clinic_id:1, name:test clinic, date:2021-08-02 start_at: 20:00:00 ends_at:20:30:00 doctor: mohamed ahmed, patient: test",
        "clinic_id:2, name:test clinic, date:2021-12-12 start_at: 12:30:00 ends_at:13:00:00 doctor: mohamed ahmed, patient: not yet"
    ]
}
    ```


