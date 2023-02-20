from django.urls import re_path
from emailer.views import emailApi

urlpatterns=[
    re_path(r'^sendemail$', emailApi.as_view())
]