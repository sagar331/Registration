from app.views import *
from rest_framework.routers import DefaultRouter
from django.urls import path,include
router = DefaultRouter()
router.register(r'register', RegisterView, basename='user')
router.register(r'login', LoginView, basename='login')
router.register(r'logout', LogOutView, basename='logout')
router.register(r'Detail', DetailViewSet, basename='Detail')
urlpatterns = router.urls