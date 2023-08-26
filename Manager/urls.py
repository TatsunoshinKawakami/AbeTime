from django.urls import path
from Manager import views

app_name = 'Manager'
urlpatterns = [
    path("", views.ManagerIndexView.as_view(), name="index"),
    path("date/<year>/<month>/<day>", views.ManagerDateView.as_view(), name='date'),
    path("signup/", views.AbeSignUpView.as_view(), name="signup"),
    path("delete/", views.AbeUserDeleteView.as_view(), name="delete"),
]
