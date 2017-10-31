# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.template import loader


def template_lab1(request):
    context = {}
    template = loader.get_template(os.path.join('lab1', 'lab1.html'))
    return HttpResponse(template.render(context, request))
