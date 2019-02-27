from django.urls import path
from .views import ProfileView, MyProfileView, DetailsPost

urlpatterns = [
    path('profile/', ProfileView.as_view()),
    path('profile/my', MyProfileView.as_view()),
    path('profile/post', DetailsPost.as_view()),
]
