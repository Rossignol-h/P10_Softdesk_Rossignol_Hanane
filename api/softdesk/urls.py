from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path, include
from rest_framework import routers

from authentication.views import Register
from project.views import ProjectViewSet

router = routers.DefaultRouter()
router.register(r"", ProjectViewSet, basename="projects")

urlpatterns = [

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', Register.as_view(), name='auth_register'),
    path('projects/', include(router.urls))

]
