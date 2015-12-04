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

def get_criteria_for_action(action):
    criteria_list = list(SaveSlotActionCriteria.objects.filter(action_id=action.id).all())
    criteria_list += list(InventoryActionCriteria.objects.filter(action_id=action.id).all())

    # now sort by a particular key
    criteria_list.sort(key = lambda criteria : criteria.order)
    return criteria_list

def save_slot_criteria_met(criteria, user):
    return SaveSlot.objects.filter(user_id=user.id, key=criteria.key, value=criteria.value).count() > 0

def inventory_criteria_met(criteria, user):
    how_many = Inventory.objects.filter(user_id=user.id, item_id=criteria.item_id).count();
    if criteria.should_have:
        return how_many > 0
    else:
        return how_many < 1

def criteria_met(criteria_list, user):
    for criteria in criteria_list:
        if type(criteria) is SaveSlotActionCriteria and not save_slot_criteria_met(criteria, user):
            return False, criteria.error_message
        elif type(criteria) is InventoryActionCriteria and not inventory_criteria_met(criteria, user):
            return False, criteria.error_message
    return True, ''

def index(request):
    command = request.GET.get('command', '')

    room_id = resolve_room_id(request)

    if command == '':
        room = Room.objects.filter(id=room_id).first()
        return build_response(room.description)

    action = find_action(room_id, command)
    if action is None:
        return build_response('Sorry, I don\'t know what you mean')

    criteria_list = get_criteria_for_action(action)

    is_met, message = criteria_met(criteria_list, request.user)

    if not is_met:
        return build_response(message);
    
    return build_response(action.message)
