from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    LoginView,
    adoption_application_view,
    RegistrationViewSet,
    ChildViewSet,
    AdoptionApplicationViewSet
)
from .views import donate_view

# DRF router for admin CRUD APIs
router = DefaultRouter()
router.register('registrations', RegistrationViewSet, basename='registration')
router.register('children', ChildViewSet, basename='child')
router.register('adoptions', AdoptionApplicationViewSet, basename='adoption')

urlpatterns = [
    # ----------- API ROUTES -----------
    path('api/', include(router.urls)),

    # ----------- PUBLIC APIs -----------
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/adopt/', adoption_application_view, name='adopt'),
    path("api/donate/", donate_view, name="donate"),
]
