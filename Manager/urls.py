from django.urls import path
from Manager import views

app_name = 'Manager'
urlpatterns = [
    path("", views.ManagerIndexView.as_view(), name="index"),
    path("date/<year>/<month>/<day>", views.ManagerDateView.as_view(), name='date'),
    path("locations/", views.LocationsManageView.as_view(), name="locations_manage"),
    path("location_delete/<int:pk>", views.LocationDeleteView.as_view(), name="location_delete"),
    path("signup/", views.AbeSignUpView.as_view(), name="signup"),
    path("delete/", views.AbeUserDeleteView.as_view(), name="delete"),
]
