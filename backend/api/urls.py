# from django.urls import path
# from . import views
# from .views import RegisterView, LoginView
# from .views import adoption_application_view
# from .views import ChildListView
# from rest_framework.routers import DefaultRouter
# from .views import RegistrationViewSet, ChildViewSet, AdoptionApplicationViewSet
# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('api/adopt/', adoption_application_view, name='adopt'),
#     path("children/", ChildListView.as_view(), name="children-list"),
# ]



# router = DefaultRouter()
# router.register('registrations', RegistrationViewSet)
# router.register('children', ChildViewSet)
# router.register('adoptions', AdoptionApplicationViewSet)

# urlpatterns = [
#     path('api/', include(router.urls)),
# ]


# myapp/urls.py

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import (
#     RegisterView,
#     LoginView,
#     adoption_application_view,
#     ChildListView,
#     RegistrationViewSet,
#     ChildViewSet,
#     AdoptionApplicationViewSet
# )

# # DRF router for admin CRUD APIs
# router = DefaultRouter()
# router.register('registrations', RegistrationViewSet, basename='registration')
# router.register('children', ChildViewSet, basename='child')
# router.register('adoptions', AdoptionApplicationViewSet, basename='adoption')

# urlpatterns = [
#      # ----------- API ROUTES -----------
#     path('api/', include(router.urls)),
#     # ----------- PUBLIC APIs -----------
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(), name='login'),
#     path('adopt/', adoption_application_view, name='adopt'),
#     path('children-list/', ChildListView.as_view(), name='children-list'),

#     # # ----------- ADMIN APIs -----------
#     # path('', include(router.urls)),  # Auto-generated routes for admin APIs
# ]


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
