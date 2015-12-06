from django.http import JsonResponse
from .models import *
import re
from .action_response import build_response

def match_command(expected_command, actual_command):
    return re.match('^' + expected_command + '$', actual_command, flags=re.IGNORECASE)

class CommonCommand:
    def command_text(self):
        return ''

    def process_request(self, request):
        actual_command = request.GET.get('command', '')

        expected_text = self.command_text()
        if re.match('^' + expected_text + '$', actual_command, flags=re.IGNORECASE):
            return self.do_side_effect(request)

    def do_side_effect(self, request):
        pass

class LookCommand(CommonCommand):
    def command_text(self):
        return 'look'

    def do_side_effect(self, request):
        current_profile = UserProfile.objects.filter(user_id=request.user.id).first()
        return build_response(current_profile.room.description)

class InventoryCommand(CommonCommand):
    def command_text(self):
        return 'inventory'

    def do_side_effect(self, request):
        inventory = Inventory.objects.filter(user_id=request.user.id)
        items = list(map(lambda i : i.item.description, inventory))
        return build_response(items)
