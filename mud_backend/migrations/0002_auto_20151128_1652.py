# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def stub_map(apps, schema_editor):
    # create some rooms
    Room = apps.get_model('mud_backend', 'Room')
    entrance_room = Room(description='You entered a castle. There is a key on the ground and a door north of you')
    entrance_room.save()
    second_room = Room(description='You are in the study. Ancient books surround you, but there\'s nothing else. The foyer is south of you')
    second_room.save()

    # create the user profile to put the user in the entrance room
    user = User(username='testuser', first_name='test', last_name='user', is_superuser=True, is_staff=True, password=make_password('password'))
    user.save()
    UserProfile = apps.get_model('mud_backend', 'UserProfile')
    profile = UserProfile(user_id=user.id, room_id=entrance_room.id)
    profile.save()

    # create the key that we can pickup
    Item = apps.get_model('mud_backend', 'Item')
    key = Item(description='A Rusty Key, engraved with ancient symbols', can_inventory=False)
    key.save()

    Action = apps.get_model('mud_backend', 'Action')
    # create the action for going from the foyer to the study
    foyer_to_study = Action(message='You entered the study', room_id=entrance_room.id, matcher='(go north|enter door)')
    foyer_to_study.save()

    # create the action for going from the study to the foyer
    study_to_foyer = Action(message='You left the study and are now in the foyer again', room_id=second_room.id, matcher='(exit|leave study|go south)')
    study_to_foyer.save()

class Migration(migrations.Migration):

    dependencies = [
        ('mud_backend', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(stub_map)
    ]
