from django.urls import path, include
from rest import views, admin
from rest.views import SemesterViewSet, User_Logout, semester_list, semester_detail, CourseViewSet, course_list, \
    course_detail, ClassViewSet, class_list, class_detail, LecturerViewSet, lecturer_list, lecturer_detail, \
    user_detail, StudentViewSet, student_list, student_detail, lecturer_id_search, is_super_user, lecturer_name_search, \
    CollegeDayViewSet, collegeday_list, enrol_student, withdraw_student, student_classes_list, \
    collegeday_detail, present_student_list, mark_present, mark_absent, absent_student_list, student_class_attendance, \
    class_student_list, email_student, lecturer_classes, available_classes, withdraw_lecturer, assign_lecturer, \
    semester_name_search, available_student_classes_list, user_id_search, user_group, student_id_search
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('semester_viewset', SemesterViewSet, 'semester_model_viewset')
router.register('course_viewset', CourseViewSet, 'course_model_viewset')
router.register('class_viewset', ClassViewSet, 'class_model_viewset')
router.register('lecturer_viewset', LecturerViewSet, 'lecturer_model_viewset')
router.register('student_viewset', StudentViewSet, 'student_model_viewset')
router.register('collegeday_viewset', CollegeDayViewSet, 'collegeday_model_viewset')

urlpatterns = router.urls
urlpatterns.append(path('auth/', obtain_auth_token))
urlpatterns.append(path('auth/logout/', User_Logout))
urlpatterns.append(path('user/<int:pk>/', user_detail))
urlpatterns.append(path('semester/', semester_list))
urlpatterns.append(path('semester/<int:pk>/', semester_detail))
urlpatterns.append(path('course/', course_list))
urlpatterns.append(path('course/<int:pk>/', course_detail))
urlpatterns.append(path('class/', class_list))
urlpatterns.append(path('class/<int:pk>/', class_detail))
urlpatterns.append(path('lecturer/', lecturer_list))
urlpatterns.append(path('lecturer/<int:pk>/', lecturer_detail))
urlpatterns.append(path('student/', student_list))
urlpatterns.append(path('student/<int:pk>/', student_detail))
urlpatterns.append(path('email_student/', email_student))
urlpatterns.append(path('collegeday/', collegeday_list))
urlpatterns.append(path('collegeday/<int:pk>/', collegeday_detail))
urlpatterns.append(path('enrollment/<int:class_id>/<int:student_id>/', enrol_student))
urlpatterns.append(path('withdraw/<int:class_id>/<int:student_id>/', withdraw_student))
urlpatterns.append(path('present/<int:collegeday_id>/<int:student_id>/', mark_present))
urlpatterns.append(path('absent/<int:collegeday_id>/<int:student_id>/', mark_absent))
urlpatterns.append(path('student_class/<int:student_id>/', student_classes_list))
urlpatterns.append(path('available_student_class/<int:student_id>/', available_student_classes_list))
urlpatterns.append(path('class_student_list/<int:pk>/', class_student_list))
urlpatterns.append(path('absent_student_list/<int:pk>/', absent_student_list))
urlpatterns.append(path('present_student_list/<int:pk>/', present_student_list))
urlpatterns.append(path('student_class_attendance/<int:class_id>/<int:student_id>/', student_class_attendance))
urlpatterns.append(path('lecturer_class_list/<int:lecturer_id>/', lecturer_classes))
urlpatterns.append(path('available_class_list/', available_classes))
urlpatterns.append(path('withdraw_lecturer/<int:class_id>/', withdraw_lecturer))
urlpatterns.append(path('assign_lecturer/<int:class_id>/<int:lecturer_id>/', assign_lecturer))
# urlpatterns.append(path('upload_students/', upload_students))

urlpatterns.append(path('lecturer_id_search/', lecturer_id_search))
urlpatterns.append(path('student_id_search/', student_id_search))
urlpatterns.append(path('lecturer_name_search/<int:pk>/', lecturer_name_search))
urlpatterns.append(path('semester_name_search/<int:pk>/', semester_name_search))
urlpatterns.append(path('is_super_user/', is_super_user))
urlpatterns.append(path('user_id_search/', user_id_search))
urlpatterns.append(path('user_group/', user_group))
