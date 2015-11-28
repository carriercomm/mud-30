from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core import serializers

from .models import *

def resolve_room_id(request):
    if request.user == None:
        return None

    current_profile = UserProfile.filter(user_id=request.user.id).first()
    if current_profile == None:
        return None

    # get the current room and try to match an action
    return current_profile.room_id

def index(request):
    command = request.GET.get('command', '')

    empty_response = JsonResponse({ 'messages' : [] })

    if command == '':
        return empty_response

    room_id = resolve_room_id(request)
    if room_id is None:
        return empty_response

    potential_actions = Action.objects.filter(room_id=room_id).all()

    response = {
        'messages' : ['a', 'b', 'c']
    }

    return JsonResponse(response)
