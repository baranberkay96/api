from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token


router = DefaultRouter()


urlpatterns = [

    url(r'', include(router.urls)),
    url(r'', include(router.urls)),
    url(r'^login', obtain_jwt_token),
    url(r'^register', views.create_user),
    url(r'^confirm_token/(?P<token>.+?)/', views.confirm_user_creation),
    url(r'^send_forget_password_email/', views.send_forget_password_email),
    url(r'^set_new_password/', views.set_new_password),
    url(r'^get_user_detail/(?P<pk>[0-9]+)$', views.get_user),
    url(r'^set_user_password/', views.set_user_password),

    ]