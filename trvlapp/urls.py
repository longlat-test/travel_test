from django.urls import path
from .views import ProfileView, MyProfileView, DetailsPost, ApiFoto, GetSubscribe, UpdateProfile, ListView, EventCRUD

urlpatterns = [
    path('getprofile/', ProfileView.as_view()),
    path('myprofile/', MyProfileView.as_view()),
    path('updaterofile/', DetailsPost.as_view()),
    path('addfoto/', ApiFoto.as_view()),
    path('getsubskribers/', GetSubscribe.as_view()),
    path('update/', UpdateProfile.as_view()),
    path('profilelist/', ListView.as_view()),
    path('createevent/', EventCRUD.as_view())


]
