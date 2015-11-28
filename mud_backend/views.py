from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core import serializers
import re
from .models import *

def build_response(*args):
    return JsonResponse({ 'messages' : args })

def resolve_room_id(request):
    if request.user == None:
        return None

    current_profile = UserProfile.objects.filter(user_id=request.user.id).first()
    if current_profile == None:
        return Room.objects.first().id

    # get the current room and try to match an action
    return current_profile.room_id

def find_action(room_id, command):
    for potential_action in Action.objects.filter(room_id=room_id).all():
        if re.match(potential_action.matcher, command, flags=re.IGNORECASE):
            return potential_action

def index(request):
    command = request.GET.get('command', '')

    room_id = resolve_room_id(request)

    if command == '':
        room = Room.objects.filter(id=room_id).first()
        return build_response(room.description)

    action = find_action(room_id, command)
    if action is None:
        return build_response('Sorry, I don\'t know what you mean')

    return build_response(action.message)
