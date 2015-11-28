from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core import serializers

def index(request):
    response = {
        'messages' : ['a', 'b', 'c']
    }
    return JsonResponse(response)
