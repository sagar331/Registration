from app.views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'register', RegisterView, basename='user')
router.register(r'login', LoginView, basename='login')
router.register(r'logout', LogOutView, basename='logout')
urlpatterns = router.urls