from django.urls import path
from User import views

app_name = 'User'
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("date/<int:year>/<int:month>/<int:day>", views.DateView.as_view(), name="date"),
    path("dateselect", views.DateSelectView.as_view(), name="date-select"),
    path("signup/", views.AbeSignUpView.as_view(), name="signup"),
    path("login/", views.AbeLoginView.as_view(), name="login"),
    path("logout/", views.AbeLogoutView.as_view(), name="logout")
]
