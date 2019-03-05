from django.urls import path
from .views import ProfileView, MyProfileView, DetailsPost, ApiFoto, GetSubscribe, UpdateProfile

urlpatterns = [
    path('getprofile/', ProfileView.as_view()),
    path('myprofile/', MyProfileView.as_view()),
    path('updaterofile/', DetailsPost.as_view()),
    path('addfoto/', ApiFoto.as_view()),
    path('getsubskribers/', GetSubscribe.as_view()),
    path('update/', UpdateProfile.as_view())

]
