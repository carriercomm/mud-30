from django.http import JsonResponse
import re
from .models import *
from .action_response import build_response

def resolve_room_id(request):
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

def perform_side_effects(action, user):
    messages = []
    for result in SaveSlotActionResult.objects.filter(action_id=action.id):
        # replace the existing save slot, if it exists. Create otherwise
        save_slot, created = SaveSlot.objects.get_or_create(user_id=user.id, key=result.key)
        save_slot.value = result.value
        save_slot.save()
        messages.append(result.message)

    for result in InventoryActionResult.objects.filter(action_id=action.id):
       inventory_item, created = Inventory.objects.get_or_create(user_id=user.id, item_id=result.item_id)
       if not result.should_have:
           inventory_item.delete()
       messages.append(result.message)

    profile = UserProfile.objects.filter(user_id=user.id).first()
    for result in RoomActionResult.objects.filter(action_id=action.id):
        profile.room_id = result.room_id
        profile.save()
        messages.append(result.room.description)

    return messages


def index(request):
    command = request.GET.get('command', '')

    room_id = resolve_room_id(request)

    action = find_action(room_id, command)
    if action is None:
        return build_response('Sorry, I don\'t know what you mean')

    criteria_list = get_criteria_for_action(action)

    is_met, message = criteria_met(criteria_list, request.user)

    if not is_met:
        return build_response(message);

    messages = perform_side_effects(action, request.user)

    return build_response(messages)
