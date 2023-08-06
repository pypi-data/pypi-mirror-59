#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [
    'django.views.generic.simple',

    # index 'home page' of the websignup app
    url(r'^$', views.WebSignupView.as_view(), name="signup_index"),
]
