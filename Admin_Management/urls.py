from django.conf.urls import url

from .views import Login, Register

urlpatterns = [
    url(r'^$', Login.as_view(),name="Login"),
    url(r'^Register/', Register.as_view(), name="Register")

]