from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    '''
    A room in which the user can be in
    '''
    description = models.TextField(max_length=140)

    def __str__(self):
        return self.description

class UserProfile(models.Model):
    '''
    Extra fields to attach to the user
    '''
    user = models.ForeignKey(User)
    room = models.ForeignKey(Room)

    def __str__(self):
        return self.user.username + ' is in room ' + self.room.id

class Item(models.Model):
    '''
    An item that the user can potentially pick up or interact with
    '''
    description = models.TextField(max_length=140)
    can_inventory = models.BooleanField(default=False)

    def __str__(self):
        return self.description

class Inventory(models.Model):
    '''
    The list of items the user has in their posession
    '''
    user = models.ForeignKey(User)
    item = models.ForeignKey(Item)

    def __str__(self):
        return self.user.username + ' has ' + self.item.description

class SaveSlot(models.Model):
    '''
    A save slot field for a particular user
    '''
    user = models.ForeignKey(User)
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=256)

    def __str__(self):
        return self.user.username + ': ' + self.key + ' = ' + self.value

class Action(models.Model):
    '''
    An action that the user can perform
    '''
    message = models.TextField(max_length=140)
    room = models.ForeignKey(Room)
    matcher = models.CharField(max_length=256)

    def __str__(self):
        return self.matcher + ' : ' + self.message

class SaveSlotActionCriteria(models.Model):
    '''
    A save slot requirement for a particular action
    '''
    action = models.ForeignKey(Action)
    order = models.IntegerField()
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=256)
    error_message = models.TextField(max_length=140)

    def __str__(self):
        return self.action.matcher + ' ' + self.key + ' = ' + self.value

class InventoryActionCriteria(models.Model):
    '''
    An inventory requirement for a particular action
    '''
    action = models.ForeignKey(Action)
    order = models.IntegerField()
    item = models.ForeignKey(Item)
    should_have = models.BooleanField(default=True)
    error_message = models.TextField(max_length=140)

    def __str__(self):
        verb = 'should have'
        if not self.should_have:
            verb = 'should not have'
        return self.action.matcher + ' ' + verb + ' ' + self.item.description 

class SaveSlotActionResult(models.Model):
    '''
    A save slot result for a particular action
    '''
    action = models.ForeignKey(Action)
    key = models.CharField(max_length=64)
    value = models.CharField(max_length=256)
    message = models.TextField(max_length=140)

    def __str__(self):
        return self.message

class InventoryActionResult(models.Model):
    '''
    A side effect from an action that updates inventory
    '''
    action = models.ForeignKey(Action)
    item = models.ForeignKey(Item)
    should_have = models.BooleanField(default=True)
    message = models.TextField(max_length=140)

    def __str__(self):
        return self.message

class RoomActionResult(models.Model):
    '''
    The updated room from a particular action
    '''
    action = models.ForeignKey(Action)
    room = models.ForeignKey(Room)

    def __str__(self):
        return self.action.matcher + ' => ' + self.room.id
