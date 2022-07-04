"""Merak URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import notifications.urls

from django.urls import include, path, re_path
from rest_framework import routers
from server import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"membre", views.MembreViewSet)
router.register(r"Admin", views.AdminViewSet)
router.register(r"Message", views.MessageViewSet)
router.register(r"Categorie", views.CategorieViewSet)
router.register(r"likes", views.LikesViewSet)
router.register(r"notifications", views.NotificationsViewSet)
router.register(r"Tag", views.TagViewSet)
router.register(r"Discussion", views.DiscussionViewSet)
router.register(r"Post", views.PostViewSet)
router.register(r"Question", views.QuestionViewSet)
router.register(r"Reponse", views.ReponseViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="FORUM API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('admin/', admin.site.urls),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
