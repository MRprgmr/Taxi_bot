from django.urls import path
from Bot.views import IndexView,LoginView


urlpatterns = [
    path('', IndexView.as_view(),name="index"),
    path('login', LoginView.as_view(),name="login"),
]