from django.urls import path
from rest_framework_swagger.views import get_swagger_view
from .views import ProfileView, MyProfileView, DetailsPost, ApiFoto, GetSubscribe, UpdateProfile, ListView, EventCRUD, Signup, Activate, Valuet, ForgotPassword, AddComment



urlpatterns = [
    path('getprofile/', ProfileView.as_view()),
    path('myprofile/', MyProfileView.as_view()),
    path('createprofile/', DetailsPost.as_view()),
    path('addfoto/', ApiFoto.as_view()),
    path('getsubskribers/', GetSubscribe.as_view()),
    path('update/', UpdateProfile.as_view()),
    path('profilelist/', ListView.as_view()),
    path('createevent/', EventCRUD.as_view()),
    path('activate/', Signup.as_view()),
    path('activated/<str:uidb64>/<str:token>', Activate.as_view()),
    path('valuet/', Valuet.as_view()),
    path('forgotpassword/', ForgotPassword.as_view()),
#    path('resetpassword/', ResetPassword.as_view()),
    path('addcomment/', AddComment.as_view())



]
