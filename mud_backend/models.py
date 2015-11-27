from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    '''
    A room in which the user can be in
    '''
    description = models.TextField(max_length=140)

class UserProfile(models.Model):
    '''
    Extra fields to attach to the user
    '''
    room = models.ForeignKey(Room)

class Item(models.Model):
    '''
    An item that the user can potentially pick up or interact with
    '''
    description = models.TextField(max_length=140)
    can_inventory = models.BooleanField(default=False)

class Inventory(models.Model):
    '''
    The list of items the user has in their posession
    '''
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)

class SaveSlot(models.Model):
    '''
    A save slot field for a particular user
    '''
    user = models.ForeignKey(User)
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=256)

class Action(models.Model):
    '''
    An action that the user can perform
    '''
    message = models.TextField(max_length=140)
    room = models.ForeignKey(Room)
    matcher = models.CharField(max_length=256)

class SaveSlotActionCriteria(models.Model):
    '''
    A save slot requirement for a particular action
    '''
    action = models.ForeignKey(Action)
    order = models.IntegerField()
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=256)
    error_message = models.TextField(max_length=140)

class InventoryActionCriteria(models.Model):
    '''
    An inventory requirement for a particular action
    '''
    action = models.ForeignKey(Action)
    order = models.IntegerField()
    inventory_item = models.ForeignKey(Inventory)
    should_have = models.BooleanField(default=True)
    error_message = models.TextField(max_length=140)

class SaveSlotActionResult(models.Model):
    '''
    A save slot result for a particular action
    '''
    action = models.ForeignKey(Action)
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=256)
    message = models.TextField(max_length=140)

class InventoryActionResult(models.Model):
    '''
    A side effect from an action that updates inventory
    '''
    action = models.ForeignKey(Action)
    inventory_item = models.ForeignKey(Inventory)
    should_have = models.BooleanField(default=True)
    message = models.TextField(max_length=140)

class RoomActionResult(models.Model):
    '''
    The updated room from a particular action
    '''
    action = models.ForeignKey(Action)
    room = models.ForeignKey(Room)
