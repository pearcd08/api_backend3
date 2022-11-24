from turtle import pd

from api_backend import settings
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils.datetime_safe import datetime
from django.views.decorators.csrf import csrf_exempt
from rest.models import Student, Semester, Course, Class, Lecturer, CollegeDay
from rest.permissions import IsLecturer, IsStudent
from rest.serializers import StudentSerializer, SemesterSerializer, CourseSerializer, ClassSerializer, \
    LecturerSerializer, UserSerializer, CollegeDaySerializer
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.admin import User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
def Index(request):
    return HttpResponse("hello world")


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def User_Logout(request):
    request.user.auth_token.delete();
    logout(request)
    return Response("User logged out successfully")


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
def user_detail(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Semester ViewSets
class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    authentication_class = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        name = request.data["name"]
        year = request.data["year"]
        try:
            semester = Semester.objects.create(name=name, year=year)
            semester.save()
            serializer = SemesterSerializer(semester)
            return Response(serializer.data)
        except:
            return Response(serializer.errors)


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def semester_list(request):
    if request.method == "GET":
        semesters = Semester.objects.all()
        serializer = SemesterSerializer(semesters, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = SemesterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def semester_detail(request, pk):
    try:
        semester = Semester.objects.get(semester_id=pk)
    except Semester.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = SemesterSerializer(semester)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = SemesterSerializer(semester, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        semester.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Course ViewSets

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_class = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        code = request.data["code"]
        name = request.data["name"]
        try:
            course = Course.objects.create(code=code, name=name)
            course.save()
            serializer = CourseSerializer(course)
            return Response(serializer.data)
        except:
            return Response(serializer.errors)


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def course_list(request):
    if request.method == "GET":
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser | IsLecturer | IsStudent])
def course_detail(request, pk):
    try:
        course = Course.objects.get(course_id=pk)
    except Course.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class viewsets

class ClassViewSet(viewsets.ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    authentication_class = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        number = request.data["number"]
        course = request.data["course"]
        semester = request.data["semester"]

        try:
            newclass = Class.objects.create(number=number, course_id=course, semester_id=semester)
            newclass.save()
            serializer = ClassSerializer(newclass)
            return Response(serializer.data)
        except:
            return Response(serializer.errors)


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser | IsLecturer])
def class_list(request):
    if request.method == "GET":
        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser | IsLecturer])
def class_detail(request, pk):
    try:
        selectedClass = Class.objects.get(class_id=pk)
    except Class.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = ClassSerializer(selectedClass)

        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ClassSerializer(selectedClass, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        selectedClass.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LecturerViewSet(viewsets.ModelViewSet):
    queryset = Lecturer.objects.all()
    serializer_class = LecturerSerializer
    authentication_class = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        username = request.data["username"]
        firstname = request.data["firstname"]
        lastname = request.data["lastname"]
        email = request.data["email"]
        password = request.data["password"]
        dob = request.data["dob"]
        try:
            user = User.objects.create(username=username, first_name=firstname, last_name=lastname, email=email)
            user.set_password(password)
            user.save()
            lecturer = Lecturer(user=user, dob=dob)
            user.groups.add(1)
            lecturer.save()
            serializer = LecturerSerializer(lecturer)
            return Response(serializer.data)
        except:
            return Response(serializer.errors)


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def lecturer_list(request):
    if request.method == "GET":
        lecturers = Lecturer.objects.all()
        serializer = LecturerSerializer(lecturers, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = LecturerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def lecturer_detail(request, pk):
    try:
        lecturer = Lecturer.objects.get(lecturer_id=pk)
    except Lecturer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = LecturerSerializer(lecturer)
        return Response(serializer.data)
    elif request.method == "PUT":
        firstname = request.data["firstname"]
        lastname = request.data["lastname"]
        dob = request.data["dob"]
        user = User.objects.get(id=lecturer.user_id)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        lecturer.dob = dob
        lecturer.save()
        serializer = LecturerSerializer(lecturer, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        user = User.objects.get(id=lecturer.user_id)
        user.delete()
        lecturer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_class = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        username = request.data["username"]
        firstname = request.data["firstname"]
        lastname = request.data["lastname"]
        email = request.data["email"]
        password = request.data["password"]
        dob = request.data["dob"]
        try:
            user = User.objects.create(username=username, first_name=firstname, last_name=lastname, email=email)
            user.set_password(password)
            user.save()
            student = Student(user=user, dob=dob)
            user.groups.add(2)
            student.save()
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        except:
            return Response(serializer.errors)


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser | IsStudent])
def student_list(request):
    if request.method == "GET":
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser | IsStudent])
def student_detail(request, pk):
    try:
        student = Student.objects.get(student_id=pk)
    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    elif request.method == "PUT":
        firstname = request.data["firstname"]
        lastname = request.data["lastname"]
        dob = request.data["dob"]
        user = User.objects.get(id=student.user_id)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        student.dob = dob
        student.save()
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        user = User.objects.get(id=student.user_id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def lecturer_id_search(request):
    userid = request.user.id
    lecturer = get_object_or_404(Lecturer, user=userid)
    lecturerid = lecturer.lecturer_id

    return Response({"lecturerid": lecturerid})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def student_id_search(request):
    userid = request.user.id
    student = get_object_or_404(Student, user=userid)
    studentid = student.student_id

    return Response({"studentid": studentid})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def lecturer_name_search(request, pk):
    lecturer = get_object_or_404(Lecturer, lecturer_id=pk)
    user = get_object_or_404(User, id=lecturer.user_id)
    firstname = user.first_name
    lastname = user.last_name

    return Response({"name": firstname + " " + lastname})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def semester_name_search(request, pk):
    semester = get_object_or_404(Semester, semester_id=pk)
    name = semester.name
    year = semester.year

    return Response({"name": name + " " + year})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@authentication_classes([TokenAuthentication])
def is_super_user(request):
    userid = request.user.id
    user = get_object_or_404(User, id=userid)
    if user.is_superuser:
        return Response({"superuser": "true"})
    else:
        return Response({"superuser": "false"})


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def user_group(request):
    userid = request.user.id
    user = get_object_or_404(User, id=userid)
    if user.groups.filter(name='Student').exists():
        return Response({"group": "student"})
    if user.groups.filter(name='Lecturer').exists():
        return Response({"group": "lecturer"})
    else:
        return Response({"group": "none"})


class CollegeDayViewSet(viewsets.ModelViewSet):
    queryset = CollegeDay.objects.all()
    serializer_class = CollegeDaySerializer
    authentication_class = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        newDate = request.data["college_date"]
        newClass = request.data["college_class"]
        try:
            collegeday = CollegeDay.objects.create(college_date=newDate, college_class_id=newClass)
            collegeday.save()
            serializer = CollegeDaySerializer(collegeday)
            return Response(serializer.data)
        except:
            return Response(serializer.errors)


@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser | IsLecturer])
def collegeday_list(request):
    if request.method == "GET":
        collegedays = CollegeDay.objects.all()
        serializer = CollegeDaySerializer(collegedays, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CollegeDaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser | IsStudent])
def student_classes_list(request, student_id):
    if request.method == "GET":
        classes = Class.objects.filter(students__student_id=student_id)
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def available_student_classes_list(request, student_id):
    classes = Class.objects.exclude(students__student_id=student_id)
    serializer = ClassSerializer(classes, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def enrol_student(request, class_id, student_id):
    selected_class = get_object_or_404(Class, class_id=class_id)
    selected_student = get_object_or_404(Student, student_id=student_id)
    selected_class.students.add(selected_student)
    serializer = ClassSerializer(selected_class)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def withdraw_student(request, class_id, student_id):
    selected_class = get_object_or_404(Class, class_id=class_id)
    selected_student = get_object_or_404(Student, student_id=student_id)
    selected_class.students.remove(selected_student)
    serializer = ClassSerializer(selected_class)
    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser | IsStudent | IsLecturer])
def class_student_list(request, pk):
    if request.method == "GET":
        selected_class = get_object_or_404(Class, class_id=pk)
        students = selected_class.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser | IsLecturer])
def absent_student_list(request, pk):
    if request.method == "GET":
        selected_collegeday = get_object_or_404(CollegeDay, collegeday_id=pk)
        class_id = selected_collegeday.college_class_id;
        selected_class = get_object_or_404(Class, class_id=class_id)
        allstudents = selected_class.students.all()
        absentstudents = []
        i = 0
        while i < len(allstudents):
            student_id = allstudents[i].student_id
            student = get_object_or_404(Student, student_id=student_id)
            if selected_collegeday.students.filter(student_id=student_id).exists():
                i = i + 1
            else:
                absentstudents.append(student)
                i = i + 1
        serializer = StudentSerializer(absentstudents, many=True)
        return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser | IsLecturer])
def present_student_list(request, pk):
    if request.method == "GET":
        selected_collegeday = get_object_or_404(CollegeDay, collegeday_id=pk)
        students = selected_collegeday.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsLecturer])
def mark_present(request, collegeday_id, student_id):
    selected_collegeday = get_object_or_404(CollegeDay, collegeday_id=collegeday_id)
    selected_student = get_object_or_404(Student, student_id=student_id)
    selected_collegeday.students.add(selected_student)
    serializer = CollegeDaySerializer(selected_collegeday)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsLecturer])
def mark_absent(request, collegeday_id, student_id):
    selected_collegeday = get_object_or_404(CollegeDay, collegeday_id=collegeday_id)
    selected_student = get_object_or_404(Student, student_id=student_id)
    selected_collegeday.students.remove(selected_student)
    serializer = CollegeDaySerializer(selected_collegeday)
    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser | IsLecturer])
def collegeday_detail(request, pk):
    if request.method == "GET":
        collegeday = CollegeDay.objects.get(collegeday_id=pk)
        serializer = CollegeDaySerializer(collegeday)
        return Response(serializer.data)
    elif request.method == "DELETE":
        collegeday = CollegeDay.objects.get(collegeday_id=pk)
        collegeday.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser | IsStudent | IsLecturer])
def student_class_attendance(request, class_id, student_id):
    total_collegedays = CollegeDay.objects.filter(college_class_id=class_id)
    attended_collegedays = CollegeDay.objects.filter(college_class_id=class_id, students__student_id=student_id)

    attendance_result = attended_collegedays.count() / total_collegedays.count()
    attendance_percentage = str(round(attendance_result * 100)) + '%'
    return Response(attendance_percentage)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsLecturer | IsAdminUser])
def email_student(request):
    if request.method == "POST":
        email = request.data["email"]
        subject = request.data["subject"]
        body = request.data["body"]
        sender_email = "gabriel_sl19798@hotmail.com"
        try:
            send_mail(subject=subject, message=body, from_email=sender_email, recipient_list=[email],
                      fail_silently=False)
            return Response("sent successfully")
        except:
            return Response("failed to send")


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser | IsLecturer])
def present_student_list(request, pk):
    if request.method == "GET":
        selected_collegeday = get_object_or_404(CollegeDay, collegeday_id=pk)
        students = selected_collegeday.students.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def assign_lecturer(request, class_id, lecturer_id):
    Class.objects.filter(class_id=class_id).update(lecturer=lecturer_id)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def withdraw_lecturer(request, class_id):
    Class.objects.filter(class_id=class_id).update(lecturer=None)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def lecturer_classes(request, lecturer_id):
    classes = Class.objects.filter(lecturer_id=lecturer_id)
    serializer = ClassSerializer(classes, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAdminUser])
def available_classes(request):
    classes = Class.objects.filter(lecturer_id=None)
    serializer = ClassSerializer(classes, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
def user_id_search(request):
    user_id = request.user.id
    lecturer = get_object_or_404(Lecturer, user_id=user_id)
    lecturer_id = lecturer.lecturer_id
    return Response({"lecturerid": lecturer_id})


# import pandas as pd
#
# @api_view(["PUT"])
# @authentication_classes([TokenAuthentication])
# def upload_students(request):
#     myfile = request.FILES.get('file')
#     excel_data = pd.read_excel(myfile)
#     data = pd.DataFrame(excel_data)
#     usernames = data["Username"].tolist()
#     firstnames = data["First Name"].tolist()
#     lastnames = data["Last Name"].tolist()
#     emails = data["Email"].tolist()
#     dobs = data["DOB"].tolist()
#     i = 0
#     while i < len(usernames):
#         username = usernames[i]
#         firstname = firstnames[i]
#         lastname = lastnames[i]
#         email = emails[i]
#         password = str(dobs[i]).split(" ")[0].replace("-", "")
#         dob = dobs[i]
#         user = User.objects.create_user(username=username)
#         user.first_name = firstname
#         user.last_name = lastname
#         user.email = email
#         user.set_password(password)
#         user.save()
#         student = Student(user=user)
#         student.dob = dob
#         user.groups.add(1)
#         student.save()
#         serializer = StudentSerializer(student)
#         i = i + 1
#         return Response(serializer.data)
