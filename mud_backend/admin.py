from django.contrib import admin

from .models import Room, Item, Action, SaveSlotActionCriteria, InventoryActionCriteria, SaveSlotActionResult, InventoryActionResult, RoomActionResult

admin.site.register(Room)
admin.site.register(Item)
admin.site.register(Action)
admin.site.register(SaveSlotActionCriteria)
admin.site.register(InventoryActionCriteria)
admin.site.register(SaveSlotActionResult)
admin.site.register(InventoryActionResult)
admin.site.register(RoomActionResult)
