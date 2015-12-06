from django.contrib import admin

from .models import *

admin.site.register(Room)
admin.site.register(Item)
admin.site.register(Action)
admin.site.register(SaveSlotActionCriteria)
admin.site.register(InventoryActionCriteria)
admin.site.register(SaveSlotActionResult)
admin.site.register(InventoryActionResult)
admin.site.register(RoomActionResult)
