from django.http import JsonResponse
from .models import *
import re

def build_response(args):
    if type(args) is not list:
        args = [args]
    return JsonResponse({ 'messages' : args })

class CommonCommands:
    def process_request(self, request):
        command = request.GET.get('command', '')

        current_profile = UserProfile.objects.filter(user_id=request.user.id).first()
        if re.match('^look$', command, flags=re.IGNORECASE):
            return build_response(current_profile.room.description)

        if re.match('^inventory', command, flags=re.IGNORECASE):
            inventory = Inventory.objects.filter(user_id=user.id)
            items = map(lambda i : i.item.description, inventory)
            return build_response(items)
